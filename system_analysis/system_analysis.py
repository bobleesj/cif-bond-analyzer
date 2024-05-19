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


def remove_structures_with_zero_counts(dict):
    structures_to_remove = []

    # Iterate over the items and check the file counts
    for formula, structures in dict.items():
        for structure_type, bonds in structures.items():
            if all(
                bond_info["bond_count"] == 0
                for bond_info in bonds.values()
            ):
                structures_to_remove.append(
                    (formula, structure_type)
                )  # Mark for removal

    # Remove the marked structure types
    for formula, structure_type in structures_to_remove:
        del dict[formula][structure_type]

    return dict


def add_bond_count_to_structure_dict(structure_dict, formula_dict):
    # Try to determine bond_count after remoivng duplicates
    # formula dict is used to get the file count
    for formula, pair_data in structure_dict.items():
        for structure, structure_data in pair_data.items():
            file_count = formula_dict[formula][structure][
                "file_count"
            ]
            print(file_count)

            for bond_pair, bond_count_data in structure_data.items():
                bond_count = bond_count_data["bond_count"]
                structure_dict[formula][structure][bond_pair][
                    "file_count"
                ] = file_count
                if file_count > 1:
                    bond_count_no_duplicates = int(
                        bond_count / file_count
                    )
                    structure_dict[formula][structure][bond_pair][
                        "bond_count_no_duplicates"
                    ] = bond_count_no_duplicates
                else:
                    structure_dict[formula][structure][bond_pair][
                        "bond_count_no_duplicates"
                    ] = bond_count
    return structure_dict


def initialize_structure_duplicate_dict(
    unique_formulas, unique_structure_types
):
    return {
        formula: {
            structure_type: {"file_count": 0}
            for structure_type in unique_structure_types
        }
        for formula in unique_formulas
    }


def initialize_system_analysis_dict(
    unique_formulas, unique_structure_types, bond_types
):
    return {
        formula: {
            structure_type: {
                bond: {
                    "bond_count": 0,
                    "bond_total_dist": 0.0,
                    "bond_avg_dist": 0.0,
                    "bond_lengths": [],
                    "bond_std_dev": 0.0,
                }
                for bond in bond_types
            }
            for structure_type in unique_structure_types
        }
        for formula in unique_formulas
    }


def add_bond_count_avg_std(
    json_file_path, structure_dict, formula_dict
):
    # Read the JSON file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Iterate through data to update dictionaries
    for bond_pair, pair_data in data.items():
        for cif_data in pair_data.values():
            file_count_updated = False  # Tracker to ensure file is counted once per bond_pair

            for data_item in cif_data:
                formula = data_item["formula"]
                structure_type = data_item["structure_type"]

                # Ensure the structure dictionary structure
                formula_info = structure_dict.setdefault(formula, {})
                structure_info = formula_info.setdefault(
                    structure_type, {}
                )
                bond_info = structure_info.setdefault(
                    bond_pair,
                    {
                        "bond_count": 0,
                        "bond_total_dist": 0.0,
                        "bond_lengths": [],
                        "bond_std_dev": 0.0,
                    },
                )

                # Update counts, distances, and store bond length
                bond_length = float(data_item["dist"])
                bond_info["bond_count"] += 1
                bond_info["bond_total_dist"] += bond_length
                bond_info["bond_lengths"].append(bond_length)

                # Calculate average and standard deviation
                if bond_info["bond_count"] > 1:
                    bond_info["bond_avg_dist"] = np.round(
                        bond_info["bond_total_dist"]
                        / bond_info["bond_count"],
                        3,
                    )
                    bond_info["bond_std_dev"] = np.round(
                        np.std(bond_info["bond_lengths"], ddof=1),
                        3,  # ddof=1 for sample standard deviation
                    )
                else:
                    bond_info["bond_avg_dist"] = bond_length
                    bond_info["bond_std_dev"] = 0.0

                # Update file count if not already done for this CIF data group
                if not file_count_updated:
                    file_counts = formula_dict.setdefault(
                        formula, {}
                    ).setdefault(structure_type, {"file_count": 0})
                    file_counts["file_count"] += 1
                    file_count_updated = True

    return structure_dict, formula_dict
