import os
import json
import time
import pandas as pd
import numpy as np
from cifkit import CifEnsemble
from cifkit.utils import string_parser
from core.util import folder, prompt
from core.util import folder
from core.prompts.progress import prompt_folder_progress
from core.prompts.intro import prompt_coordination_analysis_intro
from core.prompts.input import prompt_to_include_nested_files
from core.coordination.util import compute_delta
from core.coordination.excel import save_excel_for_connections
from core.coordination.json import save_json_for_connections


def run_coordination(script_path):
    prompt_coordination_analysis_intro()
    dir_names_with_cif = folder.get_cif_dir_paths(script_path)
    selected_dirs = prompt.get_user_input_folder_processing(
        dir_names_with_cif, ".cif"
    )

    # Would you like to include nested .cif files?
    include_nested_files = prompt_to_include_nested_files()
    process_folders(selected_dirs, include_nested_files)


def process_folders(selected_dirs, include_nested_files):
    num_selected_dirs = len(selected_dirs)

    for idx, dir_path in enumerate(selected_dirs.values(), start=1):
        prompt_folder_progress(idx, dir_path, num_selected_dirs)
        process_each_folder(dir_path, include_nested_files)


def process_each_folder(dir_path, include_nested_files):
    cif_ensemble = CifEnsemble(dir_path, add_nested=include_nested_files)

    output_dir = folder.create_folder_under_output_dir(
        dir_path, "coordination"
    )

    # Save
    save_excel_for_connections(cif_ensemble, output_dir)
    print("Preparing JSON data...")
    # Save JSON
    save_json_for_connections(cif_ensemble, output_dir)
