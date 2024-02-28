import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from itertools import permutations
import gemmi
import math
import re
import numpy as np
import sympy
from numpy import sqrt
import pandas as pd
import time

np.set_printoptions(suppress=True, precision=5)

# Global variables
loop_tags = ["_atom_site_label", "_atom_site_type_symbol",
          "_atom_site_symmetry_multiplicity", "_atom_site_Wyckoff_symbol",
          "_atom_site_fract_x", "_atom_site_fract_y","_atom_site_fract_z", "_atom_site_occupancy"]

def get_CIF_block(filename):
    # Read CIF file and return the sole block
    doc = gemmi.cif.read_file(filename)
    block = doc.sole_block()
    return block

def get_loop_values(block, loop_tags):
    # Retrieve loop values for specified tags
    loop_values = [block.find_loop(tag) for tag in loop_tags]
    return loop_values

def get_coords_after_sym_op(block, atom_site_fract_x, atom_site_fract_y, atom_site_fract_z, atom_site_label):
    # Apply space group symmetry operations to fractional coordinates
    all_coords = set()  # Use a set to store unique coordinates
    for operation in block.find_loop("_space_group_symop_operation_xyz"):
        operation = operation.replace("'", "")  # Remove single quotes
        try:
            op = gemmi.Op(operation)
            new_x, new_y, new_z = op.apply_to_xyz([atom_site_fract_x, atom_site_fract_y, atom_site_fract_z])
            new_x = round(new_x, 5)
            new_y = round(new_y, 5)
            new_z = round(new_z, 5)

            all_coords.add((new_x, new_y, new_z, atom_site_label))

        except RuntimeError as e:
            print(f"Skipping operation '{operation}': {str(e)}")

    return list(all_coords)  # Convert set back to list

def get_coords_list(block, loop_values):
    loop_length = len(loop_values[0])
    coords_list = []
    for i in range(loop_length):
        atom_site_x, atom_site_y, atom_site_z = loop_values[4][i], loop_values[5][i], loop_values[6][i]
        atom_site_label = loop_values[0][i]
        atom_type_symbol = loop_values[1][i]
        all_coords = get_coords_after_sym_op(block, float(atom_site_x), float(atom_site_y), float(atom_site_z), atom_site_label)
        coords_list.append(all_coords)
    return coords_list

def get_unit_cell_lengths_angles(block):
    cell_length_a = float(block.find_value('_cell_length_a'))
    cell_length_b = float(block.find_value('_cell_length_b'))
    cell_length_c = float(block.find_value('_cell_length_c'))

    # Cell angles in 3degrees
    cell_angle_alpha = float(block.find_value('_cell_angle_alpha'))
    cell_angle_beta = float(block.find_value('_cell_angle_beta'))
    cell_angle_gamma = float(block.find_value('_cell_angle_gamma'))

    return cell_length_a, cell_length_b, cell_length_c, cell_angle_alpha, cell_angle_beta, cell_angle_gamma

def get_radians_from_degrees(angles):
    radians = [round(np.radians(angle), 5) for angle in angles]
    return radians

def calculate_distance(point1, point2, cell_lengths, angles):
    # Convert the coordinates to floats before performing calculations
    delta_x1, delta_y1, delta_z1, label1 = list(map(float, point1[:-1])) + [point1[-1]]
    delta_x2, delta_y2, delta_z2, label2 = list(map(float, point2[:-1])) + [point2[-1]]

    result = (
        (cell_lengths[0] * (delta_x1 - delta_x2))**2 +
        (cell_lengths[1] * (delta_y1 - delta_y2))**2 +
        (cell_lengths[2] * (delta_z1 - delta_z2))**2 +
        2 * cell_lengths[1] * cell_lengths[2] * np.cos(angles[0]) * (delta_y1 - delta_y2) * (delta_z1 - delta_z2) +
        2 * cell_lengths[2] * cell_lengths[0] * np.cos(angles[1]) * (delta_z1 - delta_z2) * (delta_x1 - delta_x2) +
        2 * cell_lengths[0] * cell_lengths[1] * np.cos(angles[2]) * (delta_x1 - delta_x2) * (delta_y1 - delta_y2)
    )

    distance = np.sqrt(result)
    return distance, label1, label2

def get_points_and_labels(all_coords_list, loop_values):
    all_points = []
    unique_labels = []
    unique_atoms_tuple = []
    for i, all_coords in enumerate(all_coords_list):
        points = np.array([list(map(float, coord[:-1])) for coord in all_coords])
        atom_site_label = loop_values[0][i]
        atom_site_type = loop_values[1][i]
        # print_loop_values(loop_values, i)
        unique_labels.append(atom_site_label)
        unique_atoms_tuple.append(atom_site_type)
        all_points.extend(shift_and_append_points(points, atom_site_label))
    return list(set(all_points)), unique_labels, unique_atoms_tuple

def shift_and_append_points(points, atom_site_label):
    shifts = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1],
                        [-1, 0, 0], [0, -1, 0], [-1, -1, 0], [0, 0, -1], [1, 0, -1], [0, -1, -1], [-1, -1, -1]])
    shifted_points = points[:, None, :] + shifts[None, :, :]
    all_points = []
    for point_group in shifted_points:
        for point in point_group:
            new_point = (*np.round(point,5), atom_site_label)
            all_points.append(new_point)
    return all_points

def get_atomic_pair_list(flattened_points, cell_lengths, angles):
    atomic_info_list = []
    seen_pairs = set()  # This set will track pairs that we've already processed

    for i, point1 in enumerate(flattened_points):
        distances_from_point_i = []

        for j, point2 in enumerate(flattened_points):
            if i != j:
                pair = tuple(sorted([i, j]))  # Sort the pair so (i, j) is treated as equivalent to (j, i)
                if pair not in seen_pairs:  # Check if we've already processed this pair
                    distance, label1, label2 = calculate_distance(point1, point2, cell_lengths, angles)
                    if abs(distance) > 1e-3:  # Update the condition with the tolerance value
                        distances_from_point_i.append({
                            'point_pair': (i + 1, j + 1),
                            'labels': (label1, label2),
                            'coordinates': (point1[:3], point2[:3]),  # include coordinates
                            'distance': np.round(distance, 5)
                        })
                        seen_pairs.add(pair)  # Add the pair to the set of seen pairs

        distances_from_point_i.sort(key=lambda x: x['distance'])
        atomic_info_list.extend(distances_from_point_i)

    return atomic_info_list
def get_atom_type(label):
      return re.sub(r'([I,V,X,L,C,D,M]|[\d])+$', '', label)

def extract_formula_and_atoms(block):
    formula = block.find_pair('_chemical_formula_sum')
    # Extract the formula string
    formula_string = formula[1]
    formula_string = formula_string.replace("'", "") # Remove space
    formula_string = re.sub('[~ ]', '', formula_string) # Remove dashes
    pattern = re.compile(r"([A-Z][a-z]*)(\d*)") # Remove digits

    # This will give a list of tuples, where each tuple is an element symbol and its count.
    matches = pattern.findall(formula_string)
    unique_atoms_tuple = [(atom, int(count) if count else 1) for atom, count in matches]
    num_of_unique_atoms = len(list(set(unique_atoms_tuple)))
    return unique_atoms_tuple, num_of_unique_atoms, formula_string


def handle_user_input(directories):

    for i, directory in enumerate(directories, 1):
        print(f"{i}: {directory}")

    choice = int(input("Enter the number corresponding to the directory you want to preprocess: ")) - 1

    if choice < 0 or choice >= len(directories):
        print("Invalid choice. Please try again.")
        return None

    return directories[choice]


# GLOBAL VARIABLES
MAX_ATOMS_COUNT = 1500 # the maximum number of unique atoms to be considered to calculate the shortest distance
directories = [
    "./cif_files/test"
]

# Execute only if the script is run directly, and not imported as a module
if __name__ == "__main__":

    '''
    PART 1: Choose the folder
    '''

    directory_path = handle_user_input(directories)

    if directory_path is None:
        exit(1)

    error_files = []  # list to hold names of files that cause an error
    global_pairs_data = {}


    '''
    PART 2: Processs
    '''

    for directory_path in directories:
        print()

        # Get all the files in the directory
        files = os.listdir(directory_path)
        files = [os.path.join(directory_path, file) for file in files if file.endswith('.cif')]
        file_total_count = len(files)        
        

        # For each file in the list of files
        for filename in files:
            filename_base = os.path.basename(filename)
            
            try:
                # Record the start time for processing this file
                start_time = time.time()

                # Process CIF files and return a list of coordinates after applying symmetry operations
                CIF_block = get_CIF_block(filename)                

                # Get the unit cell lengths and angles from the CIF_block
                cell_lengths_angles = get_unit_cell_lengths_angles(CIF_block)
                unique_atoms_tuple, num_of_unique_atoms, formula_string = extract_formula_and_atoms(CIF_block)

                # Extract cell lengths and angles
                cell_length_a, cell_length_b, cell_length_c, alpha_deg, beta_deg, gamma_deg = cell_lengths_angles
                alpha_rad, beta_rad, gamma_rad = get_radians_from_degrees([alpha_deg, beta_deg, gamma_deg])

                cell_angles_rad = [alpha_rad, beta_rad, gamma_rad]
                cell_lengths = [cell_length_a, cell_length_b, cell_length_c]

                # Get loop values from CIF block
                CIF_loop_values = get_loop_values(CIF_block, loop_tags)

                # Get the list of coordinates for all atoms
                all_coords_list = get_coords_list(CIF_block, CIF_loop_values)

                # Get points and labels
                all_points, unique_labels, unique_atoms_tuple = get_points_and_labels(all_coords_list, CIF_loop_values)
                number_of_unique_points_after_op = len(all_points)

                # Get the total number of unique positions after applying symmetry operations
                number_of_unique_positions_after_symmetery_op = len(all_points)
                if number_of_unique_points_after_op >= MAX_ATOMS_COUNT:
                    print(filename_base, "has more than", MAX_ATOMS_COUNT, "unique atoms after symmetry operations in the supercell.")
                    continue

                
                # Get atomic pair information
                atomic_pair_list = get_atomic_pair_list(all_points, cell_lengths, cell_angles_rad)

                # Sort atomic pairs based on distance
                #sorted_atomic_pair_list = sorted(atomic_pair_list, key=lambda k: k['[distance]'])
                
                if num_of_unique_atoms == 3:
                    # Create a new list to store the processed pairs
                    processed_pairs = []
                    

                    for i in range(number_of_unique_points_after_op):
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
                        # print(pair["point_pair"], pair["labels"], pair["distance"])

                        atom_type_0 = get_atom_type(pair['labels'][0])
                        atom_type_1 = get_atom_type(pair['labels'][1])
                        # If the atom types are not in alphabetical order

                        if atom_type_0 > atom_type_1:
                            pair['labels'] = pair['labels'][::-1]
                            pair['point_pair'] = pair['point_pair'][::-1]
                            pair['coordinates'] = pair['coordinates'][::-1]

                        # Append the pair to the new list
                        processed_pairs_ordered.append(pair)

                    # Create an empty dictionary
                    unique_pairs_dict = {}

                    for pair in processed_pairs_ordered:
                        # Extract labels and remove any numbers or roman numerals
                        first_label = get_atom_type(pair["labels"][0])
                        second_label = get_atom_type(pair["labels"][1])

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
