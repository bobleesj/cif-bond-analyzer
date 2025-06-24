from cifkit import CifEnsemble
from core.util import folder, prompt
from core.util import folder
from core.prompts.progress import prompt_folder_progress
from core.prompts.intro import prompt_coordination_analysis_intro
from core.prompts.input import prompt_to_include_nested_files
from core.coordination.excel import save_excel_for_connections
from core.coordination.json import save_json_for_connections


def run_coordination(script_path, supercell_size=2):
    """
    Initiate the coordination analysis process. This includes prompting
    for analysis introduction, collecting directory paths with
    CIF files, and processing each selected directory.
    """

    prompt_coordination_analysis_intro()
    dir_names_with_cif = folder.get_cif_dir_names(script_path)
    selected_dirs = prompt.get_user_input_folder_processing(dir_names_with_cif, ".cif")
    # Would you like to include nested .cif files?
    include_nested_files = prompt_to_include_nested_files()
    _process_folders(selected_dirs, include_nested_files, supercell_size)


def _process_folders(selected_dirs, include_nested_files, supercell_size):
    """
    Iterate through each selected directory and process it,
    considering whether to include nested CIF files.
    """
    num_selected_dirs = len(selected_dirs)

    for idx, dir_path in enumerate(selected_dirs.values(), start=1):
        prompt_folder_progress(idx, dir_path, num_selected_dirs)
        _process_each_folder(dir_path, include_nested_files, supercell_size)


def _process_each_folder(dir_path, include_nested_files, supercell_size):
    """
    Process an individual folder to perform coordination analysis,
    including saving the results in Excel and JSON formats.
    """
    cif_ensemble = CifEnsemble(dir_path, supercell_size=supercell_size, compute_CN=True, add_nested_files=include_nested_files)
    output_dir = folder.create_folder_under_output_dir(dir_path, "coordination")

    # Save
    save_excel_for_connections(cif_ensemble, output_dir)
    print("Preparing JSON data...")
    # Save JSON
    save_json_for_connections(cif_ensemble, output_dir)
