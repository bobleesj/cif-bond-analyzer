
import os
import glob
import pytest
import time
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import filter.format as format
import click
import os
import pandas as pd
import numpy as np
import shutil
from click import style
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import util.folder as folder
import matplotlib.pyplot as plt
from util.prompt import print_intro_prompt, get_user_input_on_file_skip
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from itertools import permutations
import re


'''
File: 1144106.cif
Pair: Lu Ni  2.663 Å
Pair: Ni Si  2.315 Å
Pair: Ni Ni  0.46  Å

File: 1633275.cif
Pair: Ga Ni  1.681 Å
Pair: Ga Ho  2.947 Å
Pair: Ga Ga  0.411 Å

File: 1935431.cif
Pair: Fe Sb  2.247 Å
Pair: Sb Sb  0.485 Å
Pair: La Sb  3.289 Å
Pair: Fe Fe  2.535 Å
'''

def plot_histogram():
    print("Histogram")


def get_CIF_info(file_path, loop_tags):
    """
    Parse the CIF data from the given file path.
    """
    CIF_block = cif_parser.get_CIF_block(file_path)
    cell_lengths, cell_angles_rad = cif_parser.get_cell_lenghts_angles_rad(CIF_block)
    CIF_loop_values = cif_parser.get_loop_values(CIF_block, loop_tags)
    all_coords_list = supercell.get_coords_list(CIF_block, CIF_loop_values)
    all_points, unique_labels, unique_atoms_tuple = supercell.get_points_and_labels(all_coords_list, CIF_loop_values)
    
    return CIF_block, cell_lengths, cell_angles_rad, all_coords_list,all_points, unique_labels, unique_atoms_tuple


def main():
    print_intro_prompt()
    '''
    PART 1: Choose the folder
    '''
    MAX_ATOMS_COUNT = get_user_input_on_file_skip()
    error_files = []  # list to hold names of files that cause an error
    global_pairs_data = {}

    '''
    PART 2: Process
    '''
    script_directory = os.path.dirname(os.path.abspath(__file__))
    directory_path = folder.choose_CIF_directory(script_directory)
    cif_file_path_list = glob.glob(os.path.join(directory_path, "*.cif"))

    # For each file in the list of files
    for cif_file_path in cif_file_path_list:
        filename_base = os.path.basename(cif_file_path)            
        try:
            # Process CIF files and return a list of coordinates after applying symmetry operations
            CIF_block, cell_lengths, cell_angles_rad, all_coords_list, all_points, unique_labels, unique_atoms_tuple = get_CIF_info(cif_file_path, cif_parser.get_loop_tags())
            number_of_supercell_atoms = len(all_points)
            print(f"{filename_base} has {number_of_supercell_atoms} atoms in the supercell.")

            # Get the total number of unique positions after applying symmetry operations
            if MAX_ATOMS_COUNT < len(all_points):
                click.echo(style(f"Skipped - {filename_base} has {len(all_points)} atoms", fg="yellow"))
                continue

            # Get atomic pair information
            atomic_pair_list = supercell.get_atomic_pair_list(all_points, cell_lengths, cell_angles_rad)
            unique_atoms_tuple, num_of_unique_atoms, _ = cif_parser.extract_formula_and_atoms(CIF_block)

            if num_of_unique_atoms == 3:
                # Create a new list to store the processed pairs
                processed_pairs = []
                
                for i in range(number_of_supercell_atoms):
                    pair_point = i + 1

                    shortest_pair = None
                    shortest_distance = float('inf')

                    for pair in atomic_pair_list:
                        if pair_point in pair["point_pair"] and pair["distance"] < shortest_distance:
                            shortest_distance = pair["distance"]
                            shortest_pair = pair

                    if shortest_pair is not None:
                        processed_pairs.append(shortest_pair)
                
                processed_pairs_ordered = []
                for pair in processed_pairs:
                    atom_type_0 = cif_parser.get_atom_type(pair['labels'][0])
                    atom_type_1 = cif_parser.get_atom_type(pair['labels'][1])

                    if atom_type_0 > atom_type_1:
                        pair['labels'] = pair['labels'][::-1]
                        pair['point_pair'] = pair['point_pair'][::-1]
                        pair['coordinates'] = pair['coordinates'][::-1]

                    processed_pairs_ordered.append(pair)

                # Create an empty dictionary
                unique_pairs_dict = {}

                for pair in processed_pairs_ordered:
                    # Extract labels and remove any numbers or roman numerals
                    first_label = cif_parser.get_atom_type(pair["labels"][0])
                    second_label = cif_parser.get_atom_type(pair["labels"][1])

                    # Create a tuple of the labels
                    labels_tuple = (first_label, second_label)

                    # Initialize a new dictionary for this filename if it doesn't exist yet
                    if filename_base not in unique_pairs_dict:
                        unique_pairs_dict[filename_base] = {}

                    # If these labels have not been seen before, or if this pair is shorter than the previous pair with these labels
                    if labels_tuple not in unique_pairs_dict[filename_base] or pair["distance"] < unique_pairs_dict[filename_base][labels_tuple]["distance"]:
                        # Add this pair to the dictionary
                        unique_pairs_dict[filename_base][labels_tuple] = pair

                for filename, pairs in unique_pairs_dict.items():
                    print(f"File: {filename}")
                    global_pairs_data[filename] = {}
                    for labels, pair in pairs.items():
                        atom_1 = labels[0].ljust(3)
                        atom_2 = labels[1].ljust(3)
                        distance = str(round(pair['distance'], 3)).ljust(5)
                        print(f"Pair: {atom_1}{atom_2} {distance} Å")
                        global_pairs_data[filename][(atom_1, atom_2)] = distance
                    print()
        
        except Exception as e:
            # Print error message if any error occurred and add the problematic file to the error list
            print(f'Error processing file {filename}: {e}')
            error_files.append(filename)

    # Find the unique pairs and its count across all files
    unique_pairs_distances = {}
    for filename, pairs in global_pairs_data.items():
        for pair, distance in pairs.items():
            if pair not in unique_pairs_distances:
                unique_pairs_distances[pair] = [distance]
            else:
                unique_pairs_distances[pair].append(distance)

    '''
    PART 3: OUTPUT
    '''

    print("SUMMARY:")
    for pair, distances in unique_pairs_distances.items():
        atom_1 = pair[0].strip().ljust(3)
        atom_2 = pair[1].strip().ljust(3)
        count = len(distances)
        distances_str = ' '.join([str(round(float(dist), 3)).ljust(5) for dist in distances])
        print(f"Pair: {atom_1}-{atom_2}, Count: {count}, Distances: {distances_str} Å")

    # Extract all unique elements from the pairs
    unique_elements = list(set([element for pair in unique_pairs_distances.keys() for element in pair]))

    # Generate all possible pairs (with ordering matter)
    all_possible_pairs = list(permutations(unique_elements, 2))

    # Make sure each pair is sorted
    all_possible_pairs = [tuple(sorted(pair)) for pair in all_possible_pairs]

    # Remove duplicates after sorting
    all_possible_pairs = list(set(all_possible_pairs))

    # Sort the pairs in the data as well before comparison
    sorted_pairs_data = [tuple(sorted(pair)) for pair in unique_pairs_distances.keys()]

    # Find the pairs that are not in the data
    missing_pairs = [pair for pair in all_possible_pairs if pair not in sorted_pairs_data]

    print("Missing pairs:")
    for pair in missing_pairs:
        atom_1 = pair[0].strip().ljust(3)
        atom_2 = pair[1].strip().ljust(3)
        print(f"Pair: {atom_1}-{atom_2}")


    '''
    PART 4: PLOT
    '''

    # Prepare the subplots grid. It's a square grid that has enough cells to hold all histograms.
    grid_size = int(len(unique_pairs_distances)**0.5)
    if grid_size**2 < len(unique_pairs_distances):
        grid_size += 1

    # Set the figure size
    plt.figure(figsize=(15, 10))

    # Prepare the subplots grid. It's a square grid that has enough cells to hold all histograms.
    grid_size = int(len(unique_pairs_distances)**0.5)
    if grid_size**2 < len(unique_pairs_distances):
        grid_size += 1

    # Go through each unique pair
    for i, (pair, distances) in enumerate(unique_pairs_distances.items()):
        distances = [float(dist) for dist in distances]  # Convert distances to float

        # Compute the mean and standard deviation of the distances
        mean_value = np.mean(distances)
        std_value = np.std(distances)

        # Create a new subplot for each histogram
        plt.subplot(grid_size, grid_size, i + 1)
        plt.hist(distances, bins=20, color='steelblue', edgecolor='black')
        plt.axvline(x=mean_value, color='red', linestyle='dashed', label=f"Mean: {mean_value:.4f}\nStd Dev: {std_value:.4f}")
        lower_bound = mean_value - 3 * std_value
        upper_bound = mean_value + 3 * std_value
        plt.xlim([lower_bound, upper_bound])

        # Set x-axis tick size to exactly 4 tickers
        plt.gca().xaxis.set_major_locator(ticker.LinearLocator(numticks=5))
        plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%1.3f'))  # Display up to third decimal place

        # Ensure y-axis has integer ticks
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        plt.xlabel(f"Distance (Å): {pair[0].strip()}-{pair[1].strip()}")
        plt.ylabel("Count")
        plt.legend()
        

    plt.tight_layout(pad=3.0)  # Increase padding
    plt.savefig(directory_path + '_histograms.png', dpi=300)

    plt.show()

    # Print the total number of files that caused errors
    print(f'Total files that caused errors: {len(error_files)}')
    # Print each file that caused an error
    for file in error_files:
        print(f'File: {file}')


if __name__ == "__main__":
    main()


