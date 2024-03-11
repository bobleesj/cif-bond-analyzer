"""
Main script for processing CIF files.

This script processes CIF files in a specified directory,
performs preprocessing, bond analysis, and generates output files and plots.

Usage:
    python main.py

Author: Sangjoon Bob Lee

Date: Mar 10, 2024

"""

import os
import time
from click import style, echo
import pandas as pd

from preprocess import cif_parser, cif_parser_handler, supercell
from postprocess import bond, excel, histogram
from util import folder, prompt
from filter import occupancy


def main(is_iteractive_mode=True, dir_path=None):
    """
    Runs the Python script
    """
    prompt.print_intro_prompt()
    # PART 1: Choose the folder & get user input

    log_list = []
    file_path_list = None

    if is_iteractive_mode:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        dir_path = folder.choose_CIF_directory(script_directory)
        supercell_method = prompt.get_user_input_on_supercell_method()

        # If the user chooses no option, then it's simply 3
        if not supercell_method:
            print("\nYour default option is generating a 2-2-2 supercell for",
                "files more than 100 atoms in the unit cell.")
            supercell_method = 1

    if not is_iteractive_mode:
        file_path_list = folder.get_cif_file_path_list(dir_path)
        supercell_method = 1

    file_path_list = folder.get_cif_file_path_list(dir_path)

    # PART 2: PREPROCESS
    
    dist_mix_pair_dict = {}

    overall_start_time = time.perf_counter()
    # For each file in the list of files
    for i, file_path in enumerate(file_path_list):
        start_time = time.perf_counter()
        filename_with_ext = os.path.basename(file_path)
        filename, ext = os.path.splitext(filename_with_ext)
        num_of_atoms = None
    
        # Process CIF files and return a list of coordinates
        result = cif_parser_handler.get_cif_info(
            file_path,
            cif_parser.get_loop_tags(),
            supercell_method
        )

        CIF_loop_values = cif_parser_handler.get_cif_loop_values(
            file_path
        )

        _, lenghts, angles_rad, _, all_points, _, atom_site_list = result

        num_of_atoms = len(all_points)
        index = f"({i+1}/{len(file_path_list)})"

        echo(
            style(
                f"Processing {filename_with_ext} with "
                f"{num_of_atoms} atoms {index}", fg="yellow"
            )
        )

        atomic_pair_list = supercell.get_atomic_pair_list(
            all_points,
            lenghts,
            angles_rad
        )

        # Get atomic site mixing info -> String
        atom_site_mixing_file_info = occupancy.get_atom_site_mixing_info(
            CIF_loop_values
        )

        # Get atom site pair information
        label_pair_mixing_dict = occupancy.get_atom_site_mixing_dict(
            atom_site_mixing_file_info, CIF_loop_values
        )

        # Find the shortest pair from each reference atom
        ordered_pairs = bond.process_and_order_pairs(
            all_points,
            atomic_pair_list
        )

        # Determine unique pairs and get the shortest dist for each pair
        unique_pairs_dict = bond.get_unique_pairs_dict(
            ordered_pairs,
            filename
        )

        dist_mix_pair_dict = bond.get_dist_mix_pair_dict(
            dist_mix_pair_dict,
            unique_pairs_dict,
            label_pair_mixing_dict
        )

        elapsed_time = time.perf_counter() - start_time

        prompt.print_progress(
            filename_with_ext,
            num_of_atoms,
            elapsed_time,
            is_finished=True
        )

        data = {
            'File': filename,
            "Number of atoms in supercell": num_of_atoms,
            "Processing time (s)": round(elapsed_time, 3)
        }
        log_list.append(data)

    prompt.print_dict_in_json(dist_mix_pair_dict)

    # PART 3: OUTPUT

    # For Element-Pair Display
    dist_mix_element_pair_dict = bond.get_dist_mix_element_pair_dict(
        dist_mix_pair_dict
    )

    prompt.print_dict_in_json(dist_mix_element_pair_dict)

    missing_pairs = bond.get_sorted_missing_pairs(
        dist_mix_pair_dict
    )

    # PART 4: SAVE & PLOT

    if len(file_path_list) > 0:
        # Create a directory if needed
        output_directory_path = os.path.join(dir_path, "output")

        # Check if the output directory exists, create it if it does not
        if not os.path.exists(output_directory_path):
            os.makedirs(output_directory_path)

        # Write element-pair
        folder.write_summary_and_missing_pairs(
            dist_mix_element_pair_dict,
            missing_pairs,
            "summary-element.txt",
            dir_path
        ) 

        # Write label-pair
        folder.write_summary_and_missing_pairs(
            dist_mix_pair_dict,
            missing_pairs,
            "summary-label.txt",
            dir_path
        )

        # Save Excel file
        data = excel.write_excel_json(
            dist_mix_element_pair_dict,
            "element",
            dir_path
        )

        # Save Excel file
        data = excel.write_excel_json(
            dist_mix_pair_dict,
            "label",
            dir_path
        )

        # Draw histograms
        histogram.plot_histograms_from_data(
            dist_mix_pair_dict,
            dir_path
        )

        total_elapsed_time = time.perf_counter() - overall_start_time
        print(f"Total processing time: {total_elapsed_time:.2f}s")

        # Save log csv
        folder.save_to_csv_directory(
            dir_path,
            pd.DataFrame(log_list),
            "log"
        )

    print("\nAll files successfully processed.")


if __name__ == "__main__":
    main()
