import json
import pandas as pd
from util import prompt
from postprocess import bond_missing
from system_analysis import (
    system_analysis,
    system_analysis_excel,
    system_analysis_figure,
)


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
    system_analysis.write_json_data(
        updated_json_file_path, updated_data
    )

    print("Updated JSON data has been saved to a new file.")

    """
    Step 2. Use updated JSON to conduct system analysis
    """

    all_pairs_in_the_system = (
        bond_missing.get_all_ordered_pairs_from_list(unique_pairs)
    )

    # Generate column names based on all_pairs
    bond_types = [
        "{}-{}".format(*pair) for pair in all_pairs_in_the_system
    ]

    # Initialize dictionaries
    formula_dict = (
        system_analysis.initialize_structure_duplicate_dict(
            unique_formulas, unique_structure_types
        )
    )

    structure_dict = system_analysis.initialize_system_analysis_dict(
        unique_formulas, unique_structure_types, bond_types
    )

    # Add bond count average to structure dict
    (
        structure_dict,
        formula_dict,
    ) = system_analysis.add_bond_count_avg_std(
        updated_json_file_path, structure_dict, formula_dict
    )

    # Add the number of no duplicate bond counts to structure dict
    structure_dict = system_analysis.add_bond_count_to_structure_dict(
        structure_dict, formula_dict
    )
    # Remove structures with zero bonding count
    structure_dict = (
        system_analysis.remove_structures_with_zero_counts(
            structure_dict
        )
    )

    """
    Save Save EXCEL sheet
    """

    # Save the file
    structure_df = system_analysis_excel.create_structure_sheet(
        structure_dict
    )
    structure_df.to_excel(
        "system_analysis_structures.xlsx",
        index=False,
        sheet_name="system structures",
    )

    # Save the overview Excel sheet
    original_json_dict = system_analysis.read_json_data(
        json_file_path
    )

    overview_df = system_analysis_excel.create_overview_sheet(
        original_json_dict, all_pairs_in_the_system, structure_df
    )

    AA = bond_types[0]
    AB = bond_types[1]
    BB = bond_types[2]

    def extract_and_normalize_bond_counts(data):
        results = {}
        for formula, structures in data.items():
            if formula not in results:
                results[formula] = [
                    0,
                    0,
                    0,
                ]  # Initialize Co-Co, Co-In, In-In counts
            for structure, bonds in structures.items():
                results[formula][0] += bonds[AA][
                    "bond_count_no_duplicates"
                ]
                results[formula][1] += bonds[AB][
                    "bond_count_no_duplicates"
                ]
                results[formula][2] += bonds[BB][
                    "bond_count_no_duplicates"
                ]
        # Normalize counts to fractions of the total
        normalized_results = []
        for key, value in results.items():
            total = sum(value)
            if total > 0:
                normalized_values = tuple(x / total for x in value)
            else:
                normalized_values = tuple(
                    value
                )  # Keep as is if total is 0
            normalized_results.append((key, normalized_values))

        return normalized_results

    bond_fractions_list = extract_and_normalize_bond_counts(
        structure_dict
    )
    print(structure_df.head(20))
    print(overview_df.head(20))
    print("System analysis:")

    # Draw hexagon
    for bond_fractions in bond_fractions_list:
        system_analysis_figure.draw_hexagons(
            bond_fractions, bond_types
        )

    # Draw line figure
    system_analysis_figure.draw_rotated_hexagons_along_line(
        bond_fractions_list
    )


if __name__ == "__main__":
    conduct_system_analysis()
