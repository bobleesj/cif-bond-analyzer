import os
import json
from preprocess import cif_parser

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
            cif_file_path = os.path.join(cif_directory, f"{cif_id}.cif")
            if os.path.exists(cif_file_path):
                try:
                    block = cif_parser.get_cif_block(cif_file_path)
                    formula = clean_formula(
                        block.find_value("_chemical_formula_structural")
                    )
                    structure_type = clean_structure_type(
                        block.find_value("_chemical_name_structure_type")
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
                bond_info["file_count"] == 0 for bond_info in bonds.values()
            ):
                structures_to_remove.append(
                    (formula, structure_type)
                )  # Mark for removal

    # Remove the marked structure types
    for formula, structure_type in structures_to_remove:
        del dict[formula][structure_type]

    return dict


def add_bond_count_to_dict(system_analysis_dict, structure_duplicate_dict):
    # Try to determine bond_count after remoivng duplicates
    for formula, pair_data in system_analysis_dict.items():
        for structure, structure_data in pair_data.items():
            file_count = structure_duplicate_dict[formula][structure][
                "file_count"
            ]

            for bond_pair, bond_count_data in structure_data.items():
                bond_count = bond_count_data["bond_count"]
                system_analysis_dict[formula][structure][bond_pair][
                    "file_count"
                ] = file_count
                if file_count > 1:
                    bond_count_no_duplicates = int(bond_count / file_count)
                    system_analysis_dict[formula][structure][bond_pair][
                        "bond_count_no_duplicates"
                    ] = bond_count_no_duplicates
                else:
                    system_analysis_dict[formula][structure][bond_pair][
                        "bond_count_no_duplicates"
                    ] = bond_count
    return system_analysis_dict

def initialize_structure_duplicate_dict(unique_formulas, unique_structure_types):
    return {
        formula: {structure_type: {"file_count": 0} for structure_type in unique_structure_types}
        for formula in unique_formulas
    }

def initialize_system_analysis_dict(unique_formulas, unique_structure_types, bond_types):
    return {
        formula: {
            structure_type: {bond: {"bond_count": 0} for bond in bond_types}
            for structure_type in unique_structure_types
        }
        for formula in unique_formulas
    }

def process_json_data(json_file_path, system_analysis_dict, structure_duplicate_dict):
    # Read the JSON file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Iterate through data to update dictionaries
    for bond_pair, pair_data in data.items():
        print("Start with", bond_pair)
        for cif_id, cif_data_list in pair_data.items():
            is_file_counted = False  # Tracker to ensure file is counted once per bond_pair

            for data_item in cif_data_list:
                formula = data_item["formula"]
                structure_type = data_item["structure_type"]
                system_analysis_dict[formula][structure_type][bond_pair]["bond_count"] += 1

                if not is_file_counted:
                    structure_duplicate_dict[formula][structure_type]["file_count"] += 1
                    is_file_counted = True

    return system_analysis_dict, structure_duplicate_dict
