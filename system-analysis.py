import json
import os
import pandas as pd
from util import prompt
from preprocess import cif_parser
from postprocess import bond_missing


def remove_structures_with_zero_counts(dict):
    """
    Remove structure types from the system_analysis dictionary where all bond types
    associated with a structure type have a file count of 0.

    Parameters:
    - system_analysis: A dictionary containing the system analysis data.

    Returns:
    - A modified dictionary with the specified structure types removed.
    """

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


def conduct_system_analysis():
    print("Hello world")

    # Specify the path to the original JSON file
    json_file_path = "20240411_system_analysis/output/20240411_system_analysis_site_pairs.json"
    updated_json_file_path = "20240411_system_analysis/output/updated_20240411_system_analysis_site_pairs.json"

    unique_pairs = []
    unique_structure_types = []
    unique_formulas = []

    # Read the JSON file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Directory where .cif files are stored
    cif_directory = "20240411_system_analysis"

    """
    Step 1. Update JSON with formula and structural info
    """

    for key, site_pairs in data.items():
        print(f"Processing data for: {key}")
        unique_pairs.append(key)
        for cif_id, cif_data_list in site_pairs.items():
            cif_file_path = os.path.join(cif_directory, f"{cif_id}.cif")

            if os.path.exists(cif_file_path):
                print(f"Processing {cif_file_path}")
                try:
                    # Load the CIF file
                    block = cif_parser.get_cif_block(cif_file_path)

                    # Extract and clean the desired fields
                    chemical_formula_structural = block.find_value(
                        "_chemical_formula_structural"
                    )
                    chemical_formula_structural = (
                        chemical_formula_structural.replace("~", "")
                        .replace(" ", "")
                        .replace("'", "")
                    )

                    chemical_name_structure_type = (
                        block.find_value("_chemical_name_structure_type")
                        .split(",")[0]
                        .replace("~", "")
                    )
                    # Append to the global set
                    for pair in cif_data_list:
                        pair["formula"] = chemical_formula_structural
                        pair["structure_type"] = chemical_name_structure_type

                        unique_structure_types.append(
                            chemical_name_structure_type
                        )
                        unique_formulas.append(chemical_formula_structural)

                except Exception as e:
                    print(f"Failed to process {cif_file_path}: {e}")
            else:
                print(f"File not found: {cif_file_path}")

    # Write the updated data back to a new JSON file
    with open(updated_json_file_path, "w") as file:
        json.dump(data, file, indent=4)

    print("Updated JSON data has been saved to a new file.")

    """
    Step 2. Use updated JSON to determine
    """

    all_pairs_in_the_system = bond_missing.get_all_ordered_pairs_from_list(
        unique_pairs
    )
    # Generate column names based on all_pairs
    bond_types = ["{}-{}".format(*pair) for pair in all_pairs_in_the_system]

    # Keep track of the number of structure types for each formula
    structure_duplicate_dict = {
        formula: {
            structure_type: {
                "file_count": 0
            }  # Initialize each bond type with an empty list
            for structure_type in unique_structure_types
        }
        for formula in unique_formulas
    }

    # Initialize the dictionary with nested dictionaries for each bond type
    system_analysis_dict = {
        formula: {
            structure_type: {
                bond: {"bond_count": 0} for bond in bond_types
            }  # Initialize each bond type with an empty list
            for structure_type in unique_structure_types
        }
        for formula in unique_formulas
    }

    # Read the JSON file
    with open(updated_json_file_path, "r") as file:
        data = json.load(file)

    for bond_pair, pair_data in data.items():
        print("Start with", bond_pair)

        for cif_id, cif_data_list in pair_data.items():
            is_file_counted = False

            for data in cif_data_list:
                formula = data["formula"]
                structure_type = data["structure_type"]
                system_analysis_dict[formula][structure_type][bond_pair][
                    "bond_count"
                ] += 1

                if not is_file_counted:
                    structure_duplicate_dict[formula][structure_type][
                        "file_count"
                    ] += 1
                    is_file_counted = True

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

    """
    Save Save EXCEL
    """

    system_analysis_dict = remove_structures_with_zero_counts(
        system_analysis_dict
    )
    prompt.print_dict_in_json(system_analysis_dict)

    rows_list = []

    for formula, structures in system_analysis_dict.items():
        for structure_type, bonds in structures.items():
            # Temporary list to hold a chunk of rows
            temp_structure_rows = []

            for bond_type, bond_info in bonds.items():
                bond_count = bond_info.get("bond_count", 0)

                # Create a row for each bond type only if bond count is non-zero
                row = {
                    "Formula": formula,
                    "Structure": structure_type,
                    "Bond type": bond_type,
                    "Bond count": bond_count,
                    "Unique bond count": bond_info.get(
                        "bond_count_no_duplicates", 0
                    ),
                }
                temp_structure_rows.append(row)
            rows_list.extend(temp_structure_rows)
            rows_list.append(
                {
                    "Formula": "",
                    "Structure": "",
                    "Bond type": "",
                    "Bond count": "",
                    "Unique bond count": "",
                }
            )

    # Create DataFrame
    df = pd.DataFrame(rows_list)
    # Writing to Excel
    df.to_excel("system_analysis_v.xlsx", index=False)

    print("Excel file has been created successfully.")

    print(df.head(20))


if __name__ == "__main__":
    conduct_system_analysis()
