import json
import os
import pandas as pd
from util import prompt
from preprocess import cif_parser
from postprocess import bond_missing
from postprocess import system_analysis


def conduct_system_analysis():
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

    # Save the file
    structure_df = system_analysis.create_bond_dataframe(system_analysis_dict)
    structure_df.to_excel(
        "system_analysis_structures.xlsx",
        index=False,
        sheet_name="system structures",
    )

    # Save the overview Excel sheet
    original_json_dict = system_analysis.read_json_data(json_file_path)

    overview_df = system_analysis.create_excel_from_bond_data(
        original_json_dict, all_pairs_in_the_system, structure_df
    )

    print(structure_df.head(20))
    print(overview_df.head(20))


if __name__ == "__main__":
    conduct_system_analysis()
