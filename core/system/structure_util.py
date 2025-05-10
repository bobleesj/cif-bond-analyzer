import json
import numpy as np
from core.util import formula_parser


def read_json_data(file_path):
    """
    Read and return data from a JSON file.
    """
    with open(file_path, "r") as file:
        return json.load(file)


def initialize_pair_data():
    """
    Initialize a dictionary to store bond length data.
    """
    return {
        "bond_lengths": [],  # List to store bond lengths
        "total_bond_count": 0,  # Initialize bond count
        "avg_bond_length": 0.0,  # Initialize average bond length
    }


def init_structure_data(pairs):
    """
    Initialize structure data for bond pairs.
    """
    return {
        "files": [],
        "formulas": [],
        "file_count": 0,
        "bond_data": {
            f"{pair[0]}-{pair[1]}": initialize_pair_data()
            for pair in pairs  # Iterate in order given for pairs
        },
    }


def init_structure_dict(unique_structures, all_pairs_in_the_system):
    """
    Initialize a dictionary for storing structure-related data.
    """
    structure_dict = {
        structure: init_structure_data(all_pairs_in_the_system)
        for structure in unique_structures
    }

    return structure_dict


def add_files_and_formula(
    structure_dict,
    updated_json_file_path,
):
    """
    Add file and formula data to the structure dictionary from JSON.
    """
    json_data = read_json_data(updated_json_file_path)
    # Initialize structure_dict with nested bond data for each pair

    # Iterate through each pair and their respective datasets in the JSON
    for pair, datasets in json_data.items():
        for dataset_id, records in datasets.items():
            for record in records:
                structure = record["structure"]
                formula = record["formula"]
                tag = record["tag"]

                # Check if this structure exists in the structure_dict
                if structure in structure_dict:
                    if dataset_id not in structure_dict[structure]["files"]:
                        structure_dict[structure]["files"].append(dataset_id)
                        structure_dict[structure]["file_count"] += 1

                        if tag != "":
                            structure_dict[structure]["formulas"].append(
                                formula + "_" + tag
                            )
                        else:
                            structure_dict[structure]["formulas"].append(formula)

    return structure_dict


def get_unique_formulas_tag(structure_dict):
    """
    Extract unique formulas with tags from the structure dictionary.
    """
    formulas_with_tag = set()

    for structure in structure_dict:
        formulas = structure_dict[structure]["formulas"]
        for formula in formulas:
            formulas_with_tag.add(formula)

    return formulas_with_tag


def add_bond_lenghts_and_statistics(structure_dict, updated_json_file_path):
    """
    Add bond lengths and calculate statistics for each bond type in structures.
    """
    json_data = read_json_data(updated_json_file_path)
    for pair, datasets in json_data.items():
        for dataset_id, records in datasets.items():
            for record in records:
                structure = record["structure"]
                bond_type = pair
                bond_length = float(record["dist"])

                # Update the bond_data for the bond type
                bond_data = structure_dict[structure]["bond_data"][bond_type]
                bond_data["bond_lengths"].append(bond_length)
                bond_data["total_bond_count"] += 1

        # Calculate average bond length for each structure and bond type
        for structure, data in structure_dict.items():
            for bond_type, bond_info in data["bond_data"].items():
                bond_lengths = np.array(bond_info["bond_lengths"])

                if bond_lengths.size > 1:
                    bond_info["avg_bond_length"] = np.round(np.mean(bond_lengths), 3)
                    bond_info["std_dev_bond_length"] = np.round(
                        np.std(bond_lengths, ddof=1), 3
                    )  # Using sample standard deviation (ddof=1)
                    bond_info["variance_bond_length"] = np.round(
                        np.var(bond_lengths, ddof=1), 3
                    )  # Using sample variance (ddof=1)
    return structure_dict


def add_unique_bond_count_per_bond_type(structure_dict):
    """
    Calculate and add unique bond counts for each type in the structure.
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
    Calculate and add bond fractions for each structure based on total bonds.
    """

    for structure, data in structure_dict.items():
        bond_data = data.get("bond_data", {})
        total_bond_count = sum(info["total_bond_count"] for info in bond_data.values())

        if total_bond_count == 0:
            continue  # Avoid division by zero if no bonds are present

        # Calculate bond fractions and store in a new dictionary key
        bond_fractions = {}
        for bond_type, info in bond_data.items():
            bond_fractions[bond_type] = np.round(
                (info["total_bond_count"] / total_bond_count),
                3,
            )

        # Add the bond fractions dictionary to the structure data
        data["bond_fractions"] = bond_fractions

    return structure_dict


def extract_bond_info_per_formula(formula, structure_dict):
    """
    Extract bond data for a specified formula across different structures.
    """

    # Initialize lists to store bond labels and fractions for the input formula
    bond_fractions = []
    structures_found = []

    # Search through each structure in the dictionary
    for (
        structure_key,
        structure_info,
    ) in structure_dict.items():
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
    bond_labels = structure_info["bond_fractions"].keys()
    if structures_found:
        return bond_fractions, structures_found, bond_labels


def get_is_single_binary(unique_formulas):
    """
    Determine if all formulas represent binary compounds.
    """
    return len(formula_parser.get_unique_elements_from_formulas(unique_formulas)) == 2


def get_is_binary_mixed(unique_formulas):
    """
    Check if all formulas are binary and contain exactly three unique elements.
    """
    # Check if all formulas are binary compounds.
    is_all_binary = all(
        formula_parser.get_num_element(formula) == 2 for formula in unique_formulas
    )

    # Get the count of unique elements across all unique formulas.
    unique_elements_count = len(
        formula_parser.get_unique_elements_from_formulas(unique_formulas)
    )

    return is_all_binary and unique_elements_count == 3


def get_is_ternary(unique_formulas):
    """
    Determine if all formulas represent ternary compounds.
    """
    return all(
        formula_parser.get_num_element(formula) == 3 for formula in unique_formulas
    )


def get_is_binary_ternary_combined(unique_formulas):
    """
    Check if the set of formulas includes both binary and ternary compounds.
    """
    clean_formulas = [formula.split("_")[0] for formula in unique_formulas]

    element_counts = [
        formula_parser.get_num_element(formula) for formula in clean_formulas
    ]

    return 2 in element_counts and 3 in element_counts
