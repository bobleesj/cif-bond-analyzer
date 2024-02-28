import click
import os
import pandas as pd
from click import style
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import util.folder as folder
import filter.info as info
import shutil
from os.path import join, exists


def get_user_input():
    max_atoms_count = click.prompt('\nEnter the maximum number of atoms in the supercell (files above this number will be moved)', type=int)
    return max_atoms_count


def print_intro_prompt():
    print("Move CIF files to a separate directory if the number of atoms in the supercell exceeds the input provided by the user.")


def move_files_based_on_supercell_size(script_directory, is_interactive_mode = True, max_atoms_threshold = 1000):
    print_intro_prompt()

    global results, folder_info
    results = []

    if is_interactive_mode:
        max_atoms_threshold = get_user_input()
        folder_info = folder.choose_CIF_directory(script_directory)
    
    if not is_interactive_mode:
        folder_info = script_directory
    
    folder_name = os.path.basename(folder_info)
    filtered_folder_name = f"{folder_name}_filter_supercell_size"
    filtered_folder = join(folder_info, filtered_folder_name)

    files_lst = [join(folder_info, file) for file in os.listdir(folder_info) if file.endswith('.cif')]

    for idx, file_path in enumerate(files_lst, start=1):
        filtered_flag = False

        # Extract filename and number of atoms first
        filename_base = os.path.basename(file_path)
        CIF_block = cif_parser.get_CIF_block(file_path)
        CIF_loop_values = cif_parser.get_loop_values(CIF_block, cif_parser.get_loop_tags())
        all_coords_list = supercell.get_coords_list(CIF_block, CIF_loop_values)
        all_points, _, _ = supercell.get_points_and_labels(all_coords_list, CIF_loop_values)
        num_of_atoms = len(all_points)
        
        # Display the information
        click.echo(style(f"Processing {filename_base} with {num_of_atoms} atoms...", fg="blue"))
        if not exists(filtered_folder):
                os.mkdir(filtered_folder)
                
        if num_of_atoms > max_atoms_threshold:
            filtered_flag = True
            new_file_path = join(filtered_folder, os.path.basename(file_path))
            shutil.move(file_path, new_file_path)
            click.echo(style(f"Moved - {filename_base} has {num_of_atoms} atoms", fg="yellow"))
        

        data = {
            "CIF file": filename_base,
            "Number of atoms in supercell": num_of_atoms,
            "Filtered": filtered_flag
        }

             
        results.append(data)
        print(f"Processed {filename_base} with {num_of_atoms} atoms ({idx}/{len(files_lst)})")

    folder.save_to_csv_directory(folder_info, pd.DataFrame(results), "supercell_size")
