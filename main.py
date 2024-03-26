"""
Main script for processing CIF files.

This script processes CIF files in a specified directory,
performs preprocessing, bond analysis, and generates output files and plots.

Usage:
    python main.py

Author: Sangjoon Bob Lee

Last update: Mar 26, 2024
Release date: Mar 10, 2024

"""

import os
import time
import pandas as pd
from click import style, echo


from preprocess import cif_parser, cif_parser_handler, supercell, format
from postprocess import bond, bond_missing, excel, histogram, writer
from util import folder, prompt
from filter import occupancy


def main(is_iteractive_mode=True, dir_path=None):
    """
    Runs the Python script
    """
    # PART 1: Choose the folder & get user input
    prompt.print_intro_prompt()

    log_list = []
    file_path_list = None
    supercell_method = None

    if is_iteractive_mode:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        dir_path = folder.choose_CIF_directory(script_directory)
        supercell_method = prompt.get_user_input_on_supercell_method()

        # If the user chooses no option, then it's simply 3
        if not supercell_method:
            print(
                "\nYour default option is generating a 2-2-2 supercell for",
                "files more than 100 atoms in the unit cell.",
            )
            supercell_method = 3

    if not is_iteractive_mode:
        file_path_list = folder.get_cif_file_path_list(dir_path)
        supercell_method = 3

    file_path_list = folder.get_cif_file_path_list(dir_path)

    # PART 2: PREPROCESS

    # # Format CIF files first
    format.move_files_based_on_format_error(dir_path)
    print("\nPreprocessing has finished. Begin extracting bond lengths.\n")

    global_site_pair_dict = {}
    global_element_pair_dict = {}

    overall_start_time = time.perf_counter()
    # For each file in the list of files
    for i, file_path in enumerate(file_path_list):
        start_time = time.perf_counter()
        filename_with_ext = os.path.basename(file_path)
        filename, ext = os.path.splitext(filename_with_ext)
        num_of_atoms = None

        # Process CIF files and return a list of coordinates
        result = cif_parser_handler.get_cif_info(
            file_path, cif_parser.get_loop_tags(), supercell_method
        )

        cif_loop_values = cif_parser_handler.get_cif_loop_values(file_path)

        _, lenghts, angles_rad, _, all_points, _, _ = result

        num_of_atoms = len(all_points)
        index = f"({i+1}/{len(file_path_list)})"

        echo(
            style(
                f"Processing {filename_with_ext} with " f"{num_of_atoms} atoms {index}",
                fg="yellow",
            )
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
            all_points, lenghts, angles_rad, atom_site_mixing_dict, filename
        )

        # Get atom site dict without the numbers on the label
        atom_site_pair_dict = bond.get_atom_site_dict_with_no_number(
            atom_site_labeled_dict
        )

        # Get the shortest element-element pair
        atom_element_pair_dict = bond.get_element_dict(atom_site_pair_dict)


        elapsed_time = time.perf_counter() - start_time

        prompt.print_progress(
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

    # prompt.print_dict_in_json(global_site_pair_dict)
    # prompt.print_dict_in_json(global_element_pair_dict)
    
    # PART 3: OUTPUT
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

        # Save Excel file (1/2) with site pair
        excel.write_site_pair_dict_to_excel_json(
            global_site_pair_dict, "site", dir_path
        )
        
        # Save Excel file (2/2) with shortest element pair
        excel.write_element_pair_dict_to_excel_json(
            global_element_pair_dict, "element", dir_path
        )

        # Save text file with element pairs
        writer.write_summary_and_missing_pairs_with_element_dict(
            global_element_pair_dict,
            missing_element_pairs,
            "summary_element.txt",
            dir_path,
        )

        # Draw histograms (1/2) with site pair
        histogram.plot_site_pair_histograms(
            global_site_pair_dict, dir_path
        )

        # Draw histograms (1/2) with element pair
        histogram.plot_element_pair_histograms(
            global_element_pair_dict, dir_path
        )

        # Save log csv
        folder.save_to_csv_directory(
            dir_path, pd.DataFrame(log_list), "log"
        )
        total_elapsed_time = time.perf_counter() - overall_start_time
        print(f"Total processing time: {total_elapsed_time:.2f}s")


if __name__ == "__main__":
    main()
