import os
from cifkit import CifEnsemble
from cifkit.utils.bond_pair import (
    get_pairs_sorted_by_mendeleev,
)

from core.run import site_analysis
from core.util import prompt, folder
from core.util import formula_parser
from core.util.bond import (
    get_ordered_bond_labels_from_AB,
    get_ordered_bond_labels_from_RMX,
)
from core.system import (
    binary,
    excel,
    single,
    structure_handler,
    structure_util,
    ternary_handler,
)
from core.system import color_map
from core.system.figure_util import get_bond_fractions_data_for_figures


def run_system_analysis(script_path):
    prompt.prompt_system_analysis_intro()

    # Display folders containing up to 3 unique elements per folder
    dir_paths = folder.choose_binary_ternary_dir(script_path)

    for idx, top_dir_path in enumerate(dir_paths, start=1):
        cif_ensemble_with_nested = CifEnsemble(
            top_dir_path, add_nested_files=True
        )

        prompt.echo_folder_progress(
            idx,
            top_dir_path,
            len(dir_paths),
            cif_ensemble_with_nested.file_count,
        )
        # Process another system analysis
        conduct_system_analysis(top_dir_path, cif_ensemble_with_nested)


def conduct_system_analysis(
    top_dir_path, cif_ensemble_with_nested: CifEnsemble
):
    site_analysis.generate_save_site_data(
        [top_dir_path], add_nested_files=True
    )
    """
    Step 1. Update JSON with formula and structural info
    """

    # Read the JSON file
    updated_json_file_path = get_site_json_site_data_path(top_dir_path)

    """
    Step 2. Build dict containing bond/formula/file info per structure
    """

    output_dir = folder.create_folder_under_output_dir(
        top_dir_path, "system_analysis"
    )

    elements = cif_ensemble_with_nested.unique_elements
    unique_formulas = cif_ensemble_with_nested.unique_formulas
    all_bond_pairs = get_pairs_sorted_by_mendeleev(list(elements))
    structures = cif_ensemble_with_nested.unique_structures
    structure_dict = structure_handler.get_structure_dict(
        structures,
        all_bond_pairs,
        updated_json_file_path,
    )

    """
    Step 3. Generate Excel file
    """

    # Save Structure Analysis and Overview Excel
    excel.save_structure_analysis_excel(structure_dict, output_dir)
    excel.save_bond_overview_excel(structure_dict, all_bond_pairs, output_dir)

    """
    Step 4. Generate hexagonal figures and color maps
    """

    # Generate ordered bond pairs for 3 unique elements
    if len(elements) == 3:
        R, M, X = formula_parser.get_RMX_from_elements(elements)
        bond_pairs_ordered = get_ordered_bond_labels_from_RMX(R, M, X)

    # Generate ordered bond pairs for 2 unique elements
    if len(elements) == 2:
        A, B = formula_parser.get_AB_from_elements(elements)
        bond_pairs_ordered = get_ordered_bond_labels_from_AB(A, B)

    bond_fraction_per_structure_data = get_bond_fractions_data_for_figures(
        cif_ensemble_with_nested, structure_dict, bond_pairs_ordered
    )

    if len(elements) not in [2, 3]:
        print("Only a total of 2 or 3 elements must be found in the folder.")
        return

    is_CN_used = False

    single.draw_hexagon_for_individual_figure(
        bond_fraction_per_structure_data, output_dir, is_CN_used
    )

    is_binary = structure_util.get_is_single_binary(unique_formulas)
    is_ternary = structure_util.get_is_ternary(unique_formulas)
    is_binary_ternary_combined = structure_util.get_is_binary_ternary_combined(
        unique_formulas
    )

    # Plot binary
    if is_binary:
        binary.draw_binary_figure(
            bond_fraction_per_structure_data,
            output_dir,
            is_CN_used,
        )

    if is_ternary or is_binary_ternary_combined:
        ternary_handler.draw_ternary_figure(
            bond_fraction_per_structure_data,
            bond_pairs_ordered,
            unique_formulas,
            (R, M, X),
            output_dir,
            is_CN_used,
        )

    #     system_color.plot_ternary_color_map(
    #         unique_formulas,
    #         structure_dict,
    #         possible_bond_pairs,
    #         output_dir,
    #     )


def get_site_json_site_data_path(dir_path):
    folder_name = os.path.basename(dir_path)
    json_file_path = os.path.join(
        dir_path, "output", f"{folder_name}_site_pairs.json"
    )
    return json_file_path
