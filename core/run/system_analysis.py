import os

from cifkit import CifEnsemble
from cifkit.utils.bond_pair import get_pairs_sorted_by_mendeleev

from core.prompts import input
from core.prompts.intro import prompt_system_analysis_intro
from core.prompts.progress import prompt_folder_progress
from core.run import site_analysis
from core.system import (
    binary,
    color_map,
    excel,
    single,
    structure_handler,
    structure_util,
    ternary_handler,
)
from core.system.figure_util import get_bond_fractions_data_for_figures
from core.util import folder, formula_parser
from core.util.bond import (
    get_ordered_bond_labels_from_AB,
    get_ordered_bond_labels_from_RMX,
)


def run_system_analysis(script_path, supercell_size=2):
    prompt_system_analysis_intro()
    # Display folders containing up to 3 unique elements per folder
    dir_paths = folder.choose_binary_ternary_dir(script_path)
    # Would you like to use bond fractions in coordination numbers?
    is_CN_used = input.prompt_to_use_CN_bond_fractions()
    use_existing_json = True
    if not is_CN_used:
        use_existing_json = input.prompt_to_use_existing_json_file()
    # Process each folder
    for idx, dir_path in enumerate(dir_paths, start=1):
        prompt_folder_progress(idx, dir_path, len(dir_paths))
        _conduct_system_analysis(
            dir_path, is_CN_used, use_existing_json, supercell_size
        )


def _conduct_system_analysis(
    dir_path, is_CN_used, use_existing_json, supercell_size
):
    """Step 1.

    Read site pair json
    """
    # Read JSON - if there is no file, run Site Analysis (SA)
    run_site_analysis = False
    updated_json_file_path = get_site_json_site_data_path(dir_path)

    if not os.path.exists(updated_json_file_path):
        print(
            f"Error: File does not exist at {updated_json_file_path}."
            " Automatically run Site Analysis."
        )
        cif_ensemble_with_nested = site_analysis._generate_site_analysis_data(
            dir_path, True, supercell_size
        )
        run_site_analysis = True

    # If SA has not been run, ask whether to run based on CN or by choice.
    if not run_site_analysis:
        if is_CN_used or not use_existing_json:
            # Compute the shortest distance (heavy computation)
            cif_ensemble_with_nested = (
                site_analysis._generate_site_analysis_data(
                    dir_path, True, supercell_size
                )
            )
        else:
            cif_ensemble_with_nested = CifEnsemble(
                dir_path, add_nested_files=True
            )
    dir_path = cif_ensemble_with_nested.dir_path
    """Step 2.

    Build dict containing bond/formula/file info per structure
    """

    output_dir = folder.create_folder_under_output_dir(
        dir_path, "system_analysis"
    )

    elements = cif_ensemble_with_nested.unique_elements

    # Check whether there are only 2 or 3 elements.
    if len(elements) not in [2, 3]:
        print("Only a total of 2 or 3 elements must be found in the folder.")
        return

    formulas_no_tag = cif_ensemble_with_nested.unique_formulas
    all_bond_pairs = get_pairs_sorted_by_mendeleev(list(elements))
    structures = cif_ensemble_with_nested.unique_structures
    structure_dict = structure_handler.get_structure_dict(
        structures,
        all_bond_pairs,
        updated_json_file_path,
    )
    """Step 3.

    Generate Excel file
    """

    # Save Structure Analysis and Overview Excel
    excel.save_structure_analysis_excel(structure_dict, output_dir)
    excel.save_bond_overview_excel(structure_dict, all_bond_pairs, output_dir)
    """Step 4.

    Generate hexagonal figures and color maps
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
        cif_ensemble_with_nested,
        structure_dict,
        bond_pairs_ordered,
        is_CN_used,
    )

    is_binary = structure_util.get_is_single_binary(formulas_no_tag)
    is_binary_mixed = structure_util.get_is_binary_mixed(formulas_no_tag)
    is_ternary = structure_util.get_is_ternary(formulas_no_tag)
    is_binary_ternary_combined = structure_util.get_is_binary_ternary_combined(
        formulas_no_tag
    )

    # Plot single
    single.draw_hexagon_for_individual_figure(
        bond_fraction_per_structure_data,
        output_dir,
        elements,
        is_CN_used,
    )

    # Plot binary
    if is_binary:
        binary.draw_binary_figure(
            bond_fraction_per_structure_data,
            output_dir,
            is_CN_used,
        )
    formulas_with_tag = structure_util.get_unique_formulas_tag(structure_dict)

    if is_ternary or is_binary_ternary_combined or is_binary_mixed:
        ternary_handler.draw_ternary_figure(
            bond_fraction_per_structure_data,
            bond_pairs_ordered,
            formulas_no_tag,
            formulas_with_tag,
            (R, M, X),
            output_dir,
            is_CN_used,
        )

        color_map.plot_ternary_color_map(
            bond_fraction_per_structure_data, (R, M, X), output_dir, is_CN_used
        )


def get_site_json_site_data_path(dir_path):
    folder_name = os.path.basename(dir_path)
    json_file_path = os.path.join(
        dir_path, "output", f"{folder_name}_site_pairs.json"
    )
    return json_file_path
