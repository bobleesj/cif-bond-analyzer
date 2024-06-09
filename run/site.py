import os
import time
import pandas as pd
from click import echo

from preprocess import cif_parser_handler, format
from postprocess import bond, bond_missing, excel, histogram, writer
from util import folder, prompt
from filter import occupancy


def run_site_analysis(
    script_path, is_iteractive_mode=True, given_dir_path=None
):
    """Runs the bond extraction procedure"""
    prompt.prompt_site_analysis_intro()
    dir_names_with_cif = None
    selected_dirs = None

    if is_iteractive_mode:
        dir_names_with_cif = folder.get_cif_dir_names(script_path)

        # If no folders containing .cif files found, exit
        if not dir_names_with_cif:
            return

        selected_dirs = prompt.get_user_input_folder_processing(
            dir_names_with_cif, ".cif"
        )

    if not is_iteractive_mode:
        given_dir_path
        selected_dirs = {1: given_dir_path}

    num_selected_dirs = len(selected_dirs)
    for idx, dir_name in enumerate(selected_dirs.values(), start=1):
        overall_start_time = time.perf_counter()
        prompt.echo_folder_progress(idx, dir_name, num_selected_dirs)

        file_path_list = None
        dir_path = None
        if is_iteractive_mode:
            dir_path = os.path.join(script_path, dir_name)
        else:
            dir_path = given_dir_path

        # PART 1: Pre-process
        format.preprocess_move_files_based_on_format_error(dir_path)
        file_path_list = folder.get_file_path_list(dir_path)

        # PART 2: Process
        (
            global_site_pair_dict,
            global_element_pair_dict,
            log_list,
        ) = get_bond_data(file_path_list)

        save_outputs(
            global_site_pair_dict,
            global_element_pair_dict,
            dir_path,
            file_path_list,
            log_list,
            overall_start_time,
        )


def get_bond_data(file_path_list):
    """Gets element pair and site pair data from files"""
    # PART 2: PREPROCESS
    global_site_pair_dict = {}
    global_element_pair_dict = {}
    log_list = []
    # For each file in the list of files
    for i, file_path in enumerate(file_path_list):
        start_time = time.perf_counter()
        filename_with_ext = os.path.basename(file_path)
        filename, ext = os.path.splitext(filename_with_ext)
        num_of_atoms = None

        # Process CIF files and return a list of coordinates
        result = cif_parser_handler.get_cif_info(file_path)

        cif_loop_values = cif_parser_handler.get_cif_loop_values(file_path)

        _, lenghts, angles_rad, _, supercell_points, _, _ = result

        num_of_atoms = len(supercell_points)

        prompt.print_progress_current(
            i, filename_with_ext, supercell_points, len(file_path_list)
        )

        # Get atomic site mixing info -> String
        atom_site_mixing_file_info = occupancy.get_atom_site_mixing_info(
            cif_loop_values
        )

        # Get atom site pair information
        atom_site_mixing_dict = occupancy.get_atom_site_mixing_dict(
            atom_site_mixing_file_info, cif_loop_values
        )

        # Get atom site labeled dict
        atom_site_labeled_dict = bond.get_atom_site_labeled_dict(
            supercell_points,
            lenghts,
            angles_rad,
            atom_site_mixing_dict,
            filename,
            file_path,
        )

        # Get atom site dict without the numbers on the label
        atom_site_pair_dict = bond.get_atom_site_dict_with_no_number(
            atom_site_labeled_dict
        )

        # Get the shortest element-element pair
        atom_element_pair_dict = bond.get_element_dict(atom_site_pair_dict)

        elapsed_time = time.perf_counter() - start_time

        prompt.print_progress_finished(
            filename_with_ext,
            num_of_atoms,
            elapsed_time,
            is_finished=True,
        )

        data = {
            "File": filename,
            "Number of atoms in supercell": num_of_atoms,
            "Processing time (s)": round(elapsed_time, 3),
        }
        log_list.append(data)

        # Collect site pairs across CIF files
        global_site_pair_dict = bond.append_atom_site_dict(
            global_site_pair_dict, atom_site_pair_dict
        )
        global_element_pair_dict = bond.append_element_site_dict(
            global_element_pair_dict, atom_element_pair_dict
        )

    return global_site_pair_dict, global_element_pair_dict, log_list


def save_outputs(
    global_site_pair_dict,
    global_element_pair_dict,
    dir_path,
    file_path_list,
    log_list,
    overall_start_time,
):
    missing_element_pairs = bond_missing.get_sorted_missing_pairs(
        global_element_pair_dict
    )

    # PART 4: SAVE & PLOT
    if len(file_path_list) > 0:
        # Create a directory if needed
        output_directory_path = os.path.join(dir_path, "output")

        # Check if the output directory exists, create it if it does not
        if not os.path.exists(output_directory_path):
            os.makedirs(output_directory_path)

        excel.save_excel_json(
            global_site_pair_dict,
            global_element_pair_dict,
            dir_path,
        )

        # Save text file with element pairs
        writer.write_summary_and_missing_pairs_with_element_dict(
            global_element_pair_dict,
            missing_element_pairs,
            "summary_element.txt",
            dir_path,
        )

        echo("Generating histograms...")
        # Draw histograms
        histogram.draw_histograms(
            global_site_pair_dict,
            global_element_pair_dict,
            dir_path,
        )

        echo("Histograms saved.")

        # Save log csv
        folder.save_to_csv_directory(dir_path, pd.DataFrame(log_list), "log")
        total_elapsed_time = time.perf_counter() - overall_start_time
        echo(f"Total processing time: {total_elapsed_time:.2f}s")
