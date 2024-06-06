import os
import json
import numpy as np
import pandas as pd
import click
from preprocess import cif_parser
from util import prompt, formula_parser, sort, string_parser
from postprocess.system import system_util


def clean_formula(formula):
    return formula.replace("~", "").replace(" ", "").replace("'", "")


def clean_structure_type(structure_type):
    return structure_type.split(",")[0].replace("~", "")


def write_json_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def read_json_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def parse_data_from_json_and_file(data, cif_directory):
    unique_pairs = []
    unique_structure_types = []
    unique_formulas = []
    for key, site_pairs in data.items():
        print(f"Processing data for: {key}")
        unique_pairs.append(key)
        for cif_id, cif_data_list in site_pairs.items():
            cif_file_path = os.path.join(cif_directory, f"{cif_id}.cif")

            # Get tag information
            if os.path.exists(cif_file_path):
                try:
                    # Parse tag
                    (
                        _,
                        _,
                        tag_string,
                        _,
                    ) = cif_parser.get_phase_tag_formula_id_from_third_line(
                        cif_file_path
                    )
                    block = cif_parser.get_cif_block(cif_file_path)

                    formula = clean_formula(
                        block.find_value("_chemical_formula_structural")
                    )
                    structure_type = clean_structure_type(
                        block.find_value("_chemical_name_structure_type")
                    )
                    # Do not append tag with "rt"
                    if tag_string and tag_string != "rt":
                        formula = formula + "_" + tag_string

                    for pair in cif_data_list:
                        pair["formula"] = formula
                        pair["structure_type"] = structure_type
                    unique_structure_types.append(structure_type)
                    unique_formulas.append(formula)
                except Exception as e:
                    print(f"Failed to process {cif_file_path}: {e}")
            else:
                print(f"File not found: {cif_file_path}")

    return (
        data,
        unique_pairs,
        set(unique_structure_types),
        set(unique_formulas),
    )


def initialize_pair_data():
    return {
        "bond_lengths": [],  # List to store bond lengths
        "total_bond_count": 0,  # Initialize bond count
        "avg_bond_length": 0.0,  # Initialize average bond length
    }


def init_structure_data(pairs):
    return {
        "files": [],
        "formulas": [],
        "file_count": 0,
        "bond_data": {
            f"{pair[0]}-{pair[1]}": initialize_pair_data()
            for pair in pairs  # Iterate in order given for pairs
        },
    }


def init_structure_dict(unique_structure_types, all_pairs_in_the_system):
    print("All pairs in the system:", all_pairs_in_the_system)
    structure_dict = {
        structure: init_structure_data(all_pairs_in_the_system)
        for structure in unique_structure_types
    }

    return structure_dict


def add_files_and_formula(
    structure_dict,
    updated_json_file_path,
):
    json_data = read_json_data(updated_json_file_path)
    # Initialize structure_dict with nested bond data for each pair

    # Iterate through each pair and their respective datasets in the JSON
    for pair, datasets in json_data.items():
        for dataset_id, records in datasets.items():
            for record in records:
                structure_type = record["structure_type"]
                formula = record[
                    "formula"
                ]  # Extract the formula from the record

                # Check if this structure_type exists in the structure_dict
                if structure_type in structure_dict:
                    if (
                        dataset_id
                        not in structure_dict[structure_type]["files"]
                    ):
                        structure_dict[structure_type]["files"].append(
                            dataset_id
                        )
                        structure_dict[structure_type]["file_count"] += 1
                        structure_dict[structure_type]["formulas"].append(
                            formula
                        )  # Also append the formula

    return structure_dict


def add_bond_lenghts_and_statistics(structure_dict, updated_json_file_path):
    json_data = read_json_data(updated_json_file_path)
    for pair, datasets in json_data.items():
        for dataset_id, records in datasets.items():
            for record in records:
                structure_type = record["structure_type"]
                bond_type = pair
                bond_length = float(record["dist"])

                # Update the bond_data for the bond type
                bond_data = structure_dict[structure_type]["bond_data"][
                    bond_type
                ]
                bond_data["bond_lengths"].append(bond_length)
                bond_data["total_bond_count"] += 1

        # Calculate average bond length for each structure and bond type
        for structure, data in structure_dict.items():
            for bond_type, bond_info in data["bond_data"].items():
                bond_lengths = np.array(
                    bond_info["bond_lengths"]
                )  # Convert bond lengths to a NumPy array for easy calculations
                if bond_lengths.size > 0:
                    bond_info["avg_bond_length"] = np.round(
                        np.mean(bond_lengths), 3
                    )
                    bond_info["std_dev_bond_length"] = np.round(
                        np.std(bond_lengths, ddof=1), 3
                    )  # Using sample standard deviation (ddof=1)
                    bond_info["variance_bond_length"] = np.round(
                        np.var(bond_lengths, ddof=1), 3
                    )  # Using sample variance (ddof=1)
    return structure_dict


def add_unique_bond_count_per_bond_type(structure_dict):
    """
    Adds a unique bond count for each bond type within each structure
    in the structure_dict. The unique bond count is calculated by dividing
    the bond count of each type by the number of files in the structure.
    """
    # Iterate over each structure in the dictionary
    for structure, data in structure_dict.items():
        number_of_files = (
            len(data["files"]) if data["files"] else 1
        )  # Avoid division by zero

        # Calculate unique bond count for each bond type and add it to the bond data
        for bond_type, bond_info in data["bond_data"].items():
            bond_count = bond_info["total_bond_count"]
            unique_bond_count = (
                bond_count / number_of_files
            )  # Calculate unique bond count per file

            # Add the calculated unique bond count to the bond data
            bond_info["unique_bond_count"] = int(unique_bond_count)

    return structure_dict


def add_bond_fractions_per_structure(structure_dict):
    """
    Calculate and add bond fractions for each bond type in each structure
    in structure_dict based on the total bond count.
    """
    for structure, data in structure_dict.items():
        bond_data = data.get("bond_data", {})
        total_bond_count = sum(
            info["total_bond_count"] for info in bond_data.values()
        )

        if total_bond_count == 0:
            continue  # Avoid division by zero if no bonds are present

        # Calculate bond fractions and store in a new dictionary key
        bond_fractions = {}
        for bond_type, info in bond_data.items():
            bond_fractions[bond_type] = np.round(
                (info["total_bond_count"] / total_bond_count), 3
            )

        # Add the bond fractions dictionary to the structure data
        data["bond_fractions"] = bond_fractions

    return structure_dict


def extract_info_per_structure(structure_dict, structure_key):
    """
    Extracts formula, bond type labels, and bond fractions
    for a given structure.
    """
    info = structure_dict[structure_key]
    formulas = info.get(
        "formulas", ["N/A"]
    )  # Default to ["N/A"] if no formulas are found

    bond_labels = info["bond_fractions"].keys()
    bond_fractions = [info["bond_fractions"][bond] for bond in bond_labels]

    return (formulas, bond_labels, bond_fractions)


def parse_unique_formulas_from_structure_dict(
    structure_dict, unique_structure_types
):
    formula_set = set()
    for _, structure in enumerate(unique_structure_types):
        result = system_util.extract_info_per_structure(
            structure_dict, structure
        )
        formulas, _, _ = result
        for formula in formulas:
            formula_set.add(formula)
    return formula_set


def extract_bond_info_per_formula(formula, structure_dict):
    """
    Parses the structure and bond fractions for each formula across all
    occurrences in the dictionary.
    """

    # Initialize lists to store bond labels and fractions for the input formula
    bond_fractions = []
    structures_found = []

    # Search through each structure in the dictionary
    for structure_key, structure_info in structure_dict.items():
        # Check if the formula is in the current structure's formula list
        if formula in structure_info["formulas"]:
            # Retrieve the bond fraction data for this structure
            bond_data = structure_info.get("bond_fractions", {})
            bond_fractions_temp = []
            for bond, fraction in bond_data.items():
                bond_fractions_temp.append(fraction)
            bond_fractions.append(bond_fractions_temp)
            structures_found.append(structure_key)

    # Check if any structure was found containing the formula
    if structures_found:
        return bond_fractions, structures_found


def get_all_unique_formulas(updated_json_file_path):
    json_data = read_json_data(updated_json_file_path)
    unique_formulas = set()  # Use a set to store unique formulas

    # Iterate over the outer dictionary
    for bond_pair, entries in json_data.items():
        # Iterate over each ID in the bond pair

        for entry_list in entries.values():
            # Iterate over the list of dictionaries under each ID
            for entry in entry_list:
                formula = entry["formula"]
                unique_formulas.add(formula)  # Add formula to the set

    return list(unique_formulas)  # Convert the set back to a list if necessary


def generate_bond_pairs(elements):
    num_of_unique_elements = len(elements)

    if num_of_unique_elements == 3:
        print("3 unique elements in the system.")
        R, M, X = elements
        bond_pairs = [
            (R, R),
            (R, M),
            (M, M),
            (M, X),
            (X, X),
            (R, X),
        ]
        return bond_pairs

    elif num_of_unique_elements == 2:
        print("2 unique elements in the system")
        R, M = elements
        bond_pairs = [(R, R), (R, M), (M, M)]
        return bond_pairs
    else:
        print(
            f"Not valid. {num_of_unique_elements} unique elements founds."
            " There should be either 2 or 3 unique elements in the folder."
        )
    return


def generate_unique_pairs_from_formulas(updated_json_file_path):
    # Get unique formulas
    unique_formulas = get_all_unique_formulas(updated_json_file_path)

    # Get unique elements
    unique_elements = formula_parser.get_unique_elements_from_formulas(
        unique_formulas
    )

    # Sort unique elements by Mendeeleve
    sorted_unique_elements = sort.sort_by_mendeleev(unique_elements)
    possible_bond_pairs = generate_bond_pairs(sorted_unique_elements)
    return possible_bond_pairs


def get_is_binary(json_file_path):
    click.echo("All binary compounds are found.")
    unique_formulas = get_all_unique_formulas(json_file_path)
    return all(
        formula_parser.get_num_element(formula) == 2
        for formula in unique_formulas
    )


def get_is_ternary(json_file_path):
    click.echo("All ternary compounds are found.")
    unique_formulas = get_all_unique_formulas(json_file_path)
    return all(
        formula_parser.get_num_element(formula) == 3
        for formula in unique_formulas
    )


def get_is_binary_ternary_combined(json_file_path):
    click.echo("Files contain both binary and ternary compounds.")
    unique_formulas = get_all_unique_formulas(json_file_path)
    element_counts = [
        formula_parser.get_num_element(formula) for formula in unique_formulas
    ]
    return 2 in element_counts and 3 in element_counts


def calculate_unit_vector(center_pt, other_x, other_y):
    dx = other_x - center_pt[0]
    dy = other_y - center_pt[1]
    dist = np.sqrt(dx**2 + dy**2)
    unit_vector = None

    if dist > 0:
        unit_vector = np.array([dx, dy]) / dist
    else:
        unit_vector = np.array([0, 0])

    return unit_vector, dist


# def extract_bond_counts(structure_dict):
#     bond_count_per_formula_dict = {}
#     # Iterate over each key in the structure_dict (assuming each key is a compound name or ID)
#     for structure in structure_dict:
#         bond_data = structure_dict[structure]["bond_data"]
#         formula = structure_dict[structure]["formulas"][0]

#         # Summarize the bond counts across different data entries for the same formula
#         for bond_type in bond_data:
#             bond_count = bond_data[bond_type]["unique_bond_count"]
#             bond_count_per_formula_dict[formula][
#                 bond_type
#             ] += bond_count

#     return bond_count_per_formula_dict
