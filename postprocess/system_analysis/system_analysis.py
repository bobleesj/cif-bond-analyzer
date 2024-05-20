import os
import json
import numpy as np
import pandas as pd
from preprocess import cif_parser
from util import prompt


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


def update_json_data(data, cif_directory):
    unique_pairs = []
    unique_structure_types = []
    unique_formulas = []
    for key, site_pairs in data.items():
        print(f"Processing data for: {key}")
        unique_pairs.append(key)
        for cif_id, cif_data_list in site_pairs.items():
            cif_file_path = os.path.join(
                cif_directory, f"{cif_id}.cif"
            )
            if os.path.exists(cif_file_path):
                try:
                    block = cif_parser.get_cif_block(cif_file_path)
                    formula = clean_formula(
                        block.find_value(
                            "_chemical_formula_structural"
                        )
                    )
                    structure_type = clean_structure_type(
                        block.find_value(
                            "_chemical_name_structure_type"
                        )
                    )
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


# Function to initialize data for each pair
def initialize_pair_data():
    return {
        "bond_lengths": [],  # List to store bond lengths
        "total_bond_count": 0,  # Default bond count
        "avg_bond_length": 0.0,  # Default average bond length
    }


# Function to initialize bond data for each structure
def init_structure_data(pairs):
    return {
        "files": [],
        "formulas": [],
        "file_count": 0,
        "bond_data": {
            f"{pair[0]}-{pair[1]}": initialize_pair_data()
            for pair in pairs
        },
    }


def init_structure_dict(
    unique_structure_types, all_pairs_in_the_system
):
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
                        structure_dict[structure_type][
                            "files"
                        ].append(dataset_id)
                        structure_dict[structure_type][
                            "file_count"
                        ] += 1
                        structure_dict[structure_type][
                            "formulas"
                        ].append(
                            formula
                        )  # Also append the formula

    return structure_dict


def add_bond_lenghts_and_statistics(
    structure_dict, updated_json_file_path
):
    json_data = read_json_data(updated_json_file_path)
    for pair, datasets in json_data.items():
        for dataset_id, records in datasets.items():
            for record in records:
                structure_type = record["structure_type"]
                bond_type = pair
                bond_length = float(record["dist"])

                # Update the bond_data for the bond type
                bond_data = structure_dict[structure_type][
                    "bond_data"
                ][bond_type]
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
    Calculate and add bond fractions for each bond type in each structure in structure_dict based on the total bond count.

    :param structure_dict: Dictionary containing structure data with bond data
    :return: None (modifies the structure_dict in place)
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

        # Optionally print each structure with its bond fractions for verification
        print(
            f"Structure: {structure}, Bond Fractions: {data['bond_fractions']}"
        )

    return structure_dict
