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
    formula_dict = system_analysis.initialize_structure_duplicate_dict(
        unique_formulas, unique_structure_types
    )

    structure_dict = system_analysis.initialize_system_analysis_dict(
        unique_formulas, unique_structure_types, bond_types
    )

    # Read the JSON file
    (
        structure_dict,
        formula_dict,
    ) = system_analysis.add_no_duplicate_file_count(
        updated_json_file_path, structure_dict, formula_dict
    )

    # Add file and bond count to the structure dict
    structure_dict = system_analysis.add_bond_count_to_structure_dict(
        structure_dict, formula_dict
    )
    prompt.print_dict_in_json(structure_dict)

    # """
    # Save Save EXCEL sheet
    # """
    # # Remove structures with zero bonding count
    # structure_dict = system_analysis.remove_structures_with_zero_counts(
    #     structure_dict
    # )

    # with open(updated_json_file_path, "r") as file:
    #     updated_site_pair_dict = json.load(file)

    # # Add average, std for each bond for each structure

    # # system_analysis.add_bond_dist_to_structure_dict(
    # #     structure_dict, updated_site_pair_dict
    # # )

    # # Save the file
    # structure_df = system_analysis.create_structure_sheet(structure_dict)
    # structure_df.to_excel(
    #     "system_analysis_structures.xlsx",
    #     index=False,
    #     sheet_name="system structures",
    # )

    # # Save the overview Excel sheet
    # original_json_dict = system_analysis.read_json_data(json_file_path)

    # overview_df = system_analysis.create_overview_sheet(
    #     original_json_dict, all_pairs_in_the_system, structure_df
    # )

    # print(structure_df.head(20))
    # print(overview_df.head(20))


if __name__ == "__main__":
    conduct_system_analysis()
