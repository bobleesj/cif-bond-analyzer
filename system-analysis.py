import json
import os
import pandas as pd
from util import prompt
from preprocess import cif_parser
from postprocess import bond_missing
from postprocess import system_analysis


def conduct_system_analysis():
    print("Hello world")

    # Specify the path to the original JSON file
    json_file_path = "20240411_system_analysis/output/20240411_system_analysis_site_pairs.json"
    updated_json_file_path = "20240411_system_analysis/output/updated_20240411_system_analysis_site_pairs.json"

    # Read the JSON file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Directory where .cif files are stored
    cif_directory = "20240411_system_analysis"

    """
    Step 1. Update JSON with formula and structural info
    """

    data = system_analysis.read_json_data(json_file_path)
    (
        updated_data,
        unique_pairs,
        unique_structure_types,
        unique_formulas,
    ) = system_analysis.update_json_data(data, cif_directory)
    system_analysis.write_json_data(updated_json_file_path, updated_data)

    with open(updated_json_file_path, "w") as file:
        json.dump(data, file, indent=4)

    print("Updated JSON data has been saved to a new file.")

    """
    Step 2. Use updated JSON to conduct system analysis
    """

    all_pairs_in_the_system = bond_missing.get_all_ordered_pairs_from_list(
        unique_pairs
    )
    # Generate column names based on all_pairs
    bond_types = ["{}-{}".format(*pair) for pair in all_pairs_in_the_system]

    # Initialize dictionaries
    structure_duplicate_dict = (
        system_analysis.initialize_structure_duplicate_dict(
            unique_formulas, unique_structure_types
        )
    )
    system_analysis_dict = system_analysis.initialize_system_analysis_dict(
        unique_formulas, unique_structure_types, bond_types
    )

    # Read the JSON file
    # Process data and update dictionaries
    (
        system_analysis_dict,
        structure_duplicate_dict,
    ) = system_analysis.process_json_data(
        updated_json_file_path, system_analysis_dict, structure_duplicate_dict
    )

    system_analysis_dict = system_analysis.add_bond_count_to_dict(
        system_analysis_dict, structure_duplicate_dict
    )

    """
    Save Save EXCEL sheet
    """

    system_analysis_dict = system_analysis.remove_structures_with_zero_counts(
        system_analysis_dict
    )
    prompt.print_dict_in_json(system_analysis_dict)

    # Save the file

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

    df = pd.DataFrame(rows_list)
    df.to_excel(
        "system_analysis_v.xlsx",
        index=False,
        sheet_name="Structures in the System",
    )
    print("Excel file has been created successfully.")
    print(df.head(20))


# Task
# Save another sheet that shows all the CIF files and the bonds

if __name__ == "__main__":
    conduct_system_analysis()
