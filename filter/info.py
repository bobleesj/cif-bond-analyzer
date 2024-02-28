import click
import os
import pandas as pd
import time
from click import style
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import util.folder as folder


def get_user_input():
    click.echo("Do you want to skip any CIF files based on the number of unique atoms in the supercell?")
    skip_based_on_atoms = click.confirm('(Default: N)', default=False)
    print()

    if skip_based_on_atoms:
        click.echo("Enter the threshold for the maximum number of atoms in the supercell.")
        max_atoms_count = click.prompt('Files with atoms exceeding this count will be skipped', type=int)
    else:
        max_atoms_count = float('inf')  # A large number to essentially disable skipping
    
    compute_min_distance = click.confirm('Do you want to calculate the minimum distance? (it may require heavy computation)', default=False)
    print()
    return max_atoms_count, compute_min_distance


def save_results_to_csv(results, folder_info):
    if results:
        if 'Min distance' in results[0]:
            folder.save_to_csv_directory(folder_info, pd.DataFrame(results), "info")


def get_num_of_atoms_shortest_dist(file_path, is_dist_computed):

    CIF_block = cif_parser.get_CIF_block(file_path)
    cell_lengths, cell_angles_rad = cif_parser.get_cell_lenghts_angles_rad(CIF_block)
    print("cell_angles_rad cell_lengths", cell_angles_rad, cell_lengths)
    CIF_loop_values = cif_parser.get_loop_values(CIF_block, cif_parser.get_loop_tags())
    all_coords_list = supercell.get_coords_list(CIF_block, CIF_loop_values)
    all_points, _, _ = supercell.get_points_and_labels(all_coords_list, CIF_loop_values)
    num_of_atoms = len(all_points)
    print("num_of_atoms:", num_of_atoms)
    
    min_distance = None
    if is_dist_computed:
        atomic_pair_list = supercell.get_atomic_pair_list(all_points, cell_lengths, cell_angles_rad)
        sorted_atomic_pairs = sorted(atomic_pair_list, key=lambda x: x['distance'])
        min_distance = sorted_atomic_pairs[0]['distance']

    return num_of_atoms, min_distance
    

def get_cif_folder_info(script_directory, is_interactive_mode=True):
    global results, folder_info  # Declare both variables as global # This allows the results variable to be accessed by other functions
    results = []

    start_time = time.time()  # Start the timer
    if is_interactive_mode:
        max_atoms_count, is_dist_computed = get_user_input()
        folder_info = folder.choose_CIF_directory(script_directory)

    if not is_interactive_mode:
        folder_info = script_directory
        max_atoms_count = 10000
        is_dist_computed = True

    # folder_info = "/Users/imac/Documents/GitHub/cif-filter-copy/20240226_big_cif_files"

    files_lst = [os.path.join(folder_info, file) for file in os.listdir(folder_info) if file.endswith('.cif')]
    overall_start_time = time.time()

    for idx, file_path in enumerate(files_lst, start=1):
        start_time = time.time()
        filename_base = os.path.basename(file_path)
        num_of_atoms, min_distance = get_num_of_atoms_shortest_dist(file_path, is_dist_computed)
        click.echo(style(f"Processing {filename_base} with {num_of_atoms} atoms...", fg="blue"))
        
        if num_of_atoms > max_atoms_count:
            click.echo(style(f"Skipped - {filename_base} has {num_of_atoms} atoms", fg="yellow"))
            continue
        
        elapsed_time = time.time() - start_time

        # Append a row to the log csv file
        data = {
            "CIF file": filename_base,
            "Number of atoms in supercell": num_of_atoms,
            "Min distance": min_distance if is_dist_computed else "N/A",  # Set to "N/A" if min distance wasn't computed
            "Processing time (s)": round(elapsed_time, 3)
        }
        results.append(data)

        print(f"Processed {filename_base} with {num_of_atoms} atoms ({idx}/{len(files_lst)})")

    save_results_to_csv(results, folder_info)
    total_elapsed_time = time.time() - overall_start_time
    print(f"Total processing time for all files: {total_elapsed_time:.2f} seconds")

