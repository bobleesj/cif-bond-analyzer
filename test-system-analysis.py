import json
import pandas as pd
import numpy as np
from util import prompt, folder, formula_parser, sort
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
    # cif_dir = "20250519_SA_ternary"
    # cif_dir = "20240512_SA_binary"
    cif_dir = "20240519_ErCoIn_ternary_binary_combine"

    json_file_path = cif_dir + f"/output/{cif_dir}_site_pairs.json"
    updated_json_file_path = (
        f"{cif_dir}/output/updated_{cif_dir}_site_pairs.json"
    )

    # Read the JSON file
    with open(json_file_path, "r") as file:
        bond_data = json.load(file)

    """
    Step 1. Update JSON with formula and structural info
    """

    (
        updated_data,
        _,
        unique_structure_types,
        unique_formulas,
    ) = system_analysis.update_json_data(bond_data, cif_dir)

    system_analysis.write_json_data(
        updated_json_file_path, updated_data
    )

    output_dir = folder.create_folder_under_output_dir(
        cif_dir, "system_analysis"
    )

    # Check whether binary or ternary
    is_binary = system_analysis.get_is_binary(updated_json_file_path)
    is_ternary = system_analysis.get_is_ternary(
        updated_json_file_path
    )

    is_binary_ternary_combined = (
        system_analysis.get_is_binary_ternary_combined(
            updated_json_file_path
        )
    )

    """
    Step 2. Build dict containing bond/formula/file info per structure
    """

    possible_bond_pairs = (
        system_analysis.generate_unique_pairs_from_formulas(
            updated_json_file_path
        )
    )

    structure_dict = system_analysis_handler.get_structure_dict(
        unique_structure_types,
        possible_bond_pairs,
        updated_json_file_path,
    )

    """
    Step 3. Generate Excel file
    """
    prompt.print_dict_in_json(structure_dict)

    # Save Structure Analysis and Overview Excel
    system_analysis_excel.save_structure_analysis_excel(
        structure_dict, output_dir
    )
    system_analysis_excel.save_bond_overview_excel(
        structure_dict, possible_bond_pairs, output_dir
    )
    """
    Step 4. Generate hexagonal figures
    """
    # prompt.print_dict_in_json(structure_dict)

    if is_binary:
        system_analysis_figure.draw_binary_figure(
            structure_dict, output_dir
        )
    print("\nTernary?", is_ternary)
    print("Binary?", is_binary)
    print("Ternary and binary combined?", is_binary_ternary_combined)

    if is_ternary or is_binary_ternary_combined:
        system_analysis_figure.draw_ternary_figure(
            structure_dict,
            unique_structure_types,
            output_dir,
            is_binary_ternary_combined,
        )

        system_analysis_figure.draw_individual_hexagon(
            structure_dict,
            unique_structure_types,
            output_dir,
            is_binary,
            is_individual_hexagonal=True,
        )
    # if is_binary or is_ternary or is_binary_ternary_combined:
    #     system_analysis_figure.draw_individual_hexagon(
    #         structure_dict,
    #         unique_structure_types,
    #         output_dir,
    #         is_binary,
    #         is_individual_hexagonal=True,
    #     )


if __name__ == "__main__":
    conduct_system_analysis()
