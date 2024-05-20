import json
import pandas as pd
import numpy as np
from util import prompt, folder
from postprocess import bond_missing
from postprocess.system_analysis import (
    system_analysis,
    system_analysis_excel,
    system_analysis_figure,
    system_analysis_handler,
)

# Set the option to display all columns
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


def conduct_system_analysis():
    # cif_directory = "20240411_system_analysis"
    # json_file_path = "20240411_system_analysis/output/20240411_system_analysis_site_pairs.json"
    # updated_json_file_path = "20240411_system_analysis/output/updated_20240411_system_analysis_site_pairs.json"

    json_file_path = (
        "20250519_ErCoIn_SA/output/20250519_ErCoIn_SA_site_pairs.json"
    )
    updated_json_file_path = "20250519_ErCoIn_SA/output/updated_20250519_ErCoIn_SA_site_pairs.json"
    cif_directory = "20250519_ErCoIn_SA"
    # Read the JSON file
    with open(json_file_path, "r") as file:
        bond_data = json.load(file)

    """
    Step 1. Update JSON with formula and structural info
    """

    (
        updated_data,
        unique_pairs,
        unique_structure_types,
        _,
    ) = system_analysis.update_json_data(bond_data, cif_directory)

    system_analysis.write_json_data(
        updated_json_file_path, updated_data
    )

    """
    Step 2. Build dict containing bond/formula/file info per structure
    """
    all_pairs_in_the_system = (
        bond_missing.get_all_ordered_pairs_from_list(unique_pairs)
    )
    structure_dict = system_analysis_handler.get_structure_dict(
        unique_structure_types,
        all_pairs_in_the_system,
        updated_json_file_path,
    )

    """
    Step 3. Generate Excel file
    """
    prompt.print_dict_in_json(structure_dict)

    data = []
    structure_list = []

    # Populate the data list with structured data from the dictionary
    for structure, info in structure_dict.items():
        first_formula = (
            info["formulas"][0] if info["formulas"] else "N/A"
        )
        structure_list.append(
            structure
        )  # Keep track of structure changes

        # Only add the formula and structure once, then add empty strings in their place
        first_row = True
        for bond_type, bond_info in info["bond_data"].items():
            row = [
                first_formula if first_row else "",
                structure if first_row else "",
                bond_type,
                bond_info["unique_bond_count"],
                bond_info["total_bond_count"],
                bond_info["avg_bond_length"],
                bond_info.get("std_dev_bond_length", 0)
                if not np.isnan(
                    bond_info.get("std_dev_bond_length", 0)
                )
                else 0,
                bond_info.get("variance_bond_length", 0)
                if not np.isnan(
                    bond_info.get("variance_bond_length", 0)
                )
                else 0,
            ]
            data.append(row)
            first_row = False

        # Add an empty row to visually separate structures
        data.append([""] * 8)  # Assuming there are 8 columns

    # Create a DataFrame
    df = pd.DataFrame(
        data,
        columns=[
            "Formula",
            "Structure Type",
            "Bond Type",
            "Unique Bond Count",
            "Total Bond Count",
            "Average Bond Length",
            "Standard Deviation",
            "Variance",
        ],
    )

    # Save DataFrame to an Excel file
    df.to_excel("formatted_bond_data.xlsx", index=False)

    """
    Step 4. Generate hexagonal figures
    """
    # # Draw hexagon
    # for bond_fractions in bond_fractions_list:
    #     system_analysis_figure.draw_hexagons(
    #         bond_fractions, bond_types
    #     )

    # # Draw line figure
    # system_analysis_figure.draw_rotated_hexagons_along_line(
    #     bond_fractions_list
    # )


if __name__ == "__main__":
    conduct_system_analysis()
