from cifkit import CifEnsemble
from click import echo

from core.prompts.input import prompt_to_include_nested_files
from core.prompts.intro import prompt_site_analysis_intro
from core.prompts.progress import prompt_folder_progress
from core.site import bond_missing, excel
from core.site import handler as site_handler
from core.site import histogram, writer
from core.util import folder, prompt


def run_site_analysis(script_path, supercell_size=2):
    """Execute the site analysis sequence including directory selection
    and initiating the analysis on selected folders."""
    prompt_site_analysis_intro()
    # Which folders would you like to process?
    dir_names_with_cif = folder.get_cif_dir_names(script_path)
    selected_dirs = prompt.get_user_input_folder_processing(
        dir_names_with_cif, ".cif"
    )
    # Would you like to include nested .cif files?
    add_nested = prompt_to_include_nested_files()
    # Process each folder selected
    num_selected_dirs = len(selected_dirs)
    for idx, (_, dir_path) in enumerate(selected_dirs.items(), start=1):
        prompt_folder_progress(idx, dir_path, num_selected_dirs)
        _generate_site_analysis_data(dir_path, add_nested, supercell_size)


def _generate_site_analysis_data(
    dir_path, add_nested, supercell_size
) -> CifEnsemble:
    """Conduct site analysis on a specified directory, handling CIF
    files and generating summary outputs and visualizations."""
    cif_ensemble = CifEnsemble(
        dir_path, add_nested_files=add_nested, supercell_size=supercell_size
    )
    site_unique_site_pair_data = (
        site_handler.get_site_pair_data_ordered_by_mendeleev(cif_ensemble)
    )
    site_unique_element_pair_data = (
        site_handler.filter_with_minimum_distance_per_file(
            site_unique_site_pair_data
        )
    )
    missing_element_pairs = bond_missing.get_sorted_missing_pairs(
        site_unique_element_pair_data
    )
    # PART 4: SAVE & PLOT
    excel.save_excel_json(
        site_unique_site_pair_data,
        site_unique_element_pair_data,
        dir_path,
    )

    # Save text file with element pairs
    writer.write_summary_and_missing_pairs_with_element_dict(
        site_unique_element_pair_data,
        missing_element_pairs,
        "summary_element.txt",
        dir_path,
    )

    echo("Generating histograms...")
    # Draw histograms
    histogram.draw_histograms(
        site_unique_site_pair_data,
        site_unique_element_pair_data,
        dir_path,
    )
    echo("Histograms saved.")
    return cif_ensemble
