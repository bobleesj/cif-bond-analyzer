
import os
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import preprocess.supercell_handler as supercell_handler
import preprocess.cif_parser_handler as cif_parser_handler
import postprocess.bond as bond
import click
import os
import pandas as pd
import time
from click import style
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import os
import util.folder as folder
import util.prompt as prompt
from itertools import permutations
import postprocess.histogram as histogram

# def get_shortest_distanc_pair_tuple_list_per_file():

def main():
    prompt.print_intro_prompt()

    '''
    PART 1: Choose the folder & get user input
    '''
    error_files = []  # list to hold names of files that cause an error
    global_pairs_data = {}

    global results
    results = []

    script_directory = os.path.dirname(os.path.abspath(__file__))
    directory_path = folder.choose_CIF_directory(script_directory)
    cif_file_path_list = folder.get_cif_file_path_list_from_directory(directory_path)
    # MAX_ATOMS_COUNT = prompt.get_user_input_on_file_skip()
    supercell_generation_method_for_above_200_atoms = prompt.get_user_input_on_supercell_generation_method()

    # If the user chooses no option, then it's simply 3
    if not supercell_generation_method_for_above_200_atoms:
        print("\nYour default option is generating a 2-2-2 supercell for files with more than 200 atoms in the unit cell.")
        supercell_generation_method_for_above_200_atoms = 3

    '''
    PART 2: PREPROCESS
    '''

    # For each file in the list of files
    for i, cif_file_path in enumerate(cif_file_path_list):
        start_time = time.time()
        overall_start_time = time.time()
        filename = os.path.basename(cif_file_path)      
        num_of_atoms = None      
        try:
            # Process CIF files and return a list of coordinates after applying symmetry operations
            _, cell_lengths, cell_angles_rad, _,all_points, _, atom_site_list = cif_parser_handler.get_CIF_info(
                cif_file_path,
                cif_parser.get_loop_tags(),
                supercell_generation_method_for_above_200_atoms
                )
            num_of_atoms = len(all_points)
            click.echo(style(f"Processing {filename} with {num_of_atoms} atoms ({i+1}/{len(cif_file_path_list)})", fg="black"))

            # Get the total number of unique positions after applying symmetry operations
            # if MAX_ATOMS_COUNT < num_of_atoms:
            #     click.echo(style(f"Skipped - {filename} has {num_of_atoms} atoms", fg="yellow"))
            #     continue

            atomic_pair_list = supercell.get_atomic_pair_list(all_points, cell_lengths, cell_angles_rad)
            is_binary_file = len(set(atom_site_list)) == 2
            is_ternary_file = len(set(atom_site_list)) == 3
            is_quaternary_file = len(set(atom_site_list)) == 4

            if is_binary_file or is_ternary_file or is_quaternary_file:
                # Create a new list to store the processed pairs
                processed_pairs = []
                
                for i in range(len(all_points)):
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

                    first_label =  pair["labels"][0]
                    second_label = pair["labels"][1]

                    # Create a tuple of the labels
                    labels_tuple = (first_label, second_label)

                    # Initialize a new dictionary for this filename if it doesn't exist yet
                    if filename not in unique_pairs_dict:
                        unique_pairs_dict[filename] = {}

                    # If these labels have not been seen before, or if this pair is shorter than the previous pair with these labels
                    if labels_tuple not in unique_pairs_dict[filename] or pair["distance"] < unique_pairs_dict[filename][labels_tuple]["distance"]:
                        # Add this pair to the dictionary
                        unique_pairs_dict[filename][labels_tuple] = pair

                for filename, pairs in unique_pairs_dict.items():
                    global_pairs_data[filename] = {}
                    print("*Print all pairs with labels for debugging.")
                    print("*Only the unique shortest pair will be written to the txt file.")
                    for labels, pair in pairs.items():
                        atom_1 = cif_parser.get_atom_type(labels[0])
                        atom_2 = cif_parser.get_atom_type(labels[1])
                        atom_1 = labels[0]
                        atom_2 = labels[1]
                        distance = str(round(pair['distance'], 3)).ljust(5)
                        print(f"Pair: {atom_1}-{atom_2} {distance} Å")
                        global_pairs_data[filename][(atom_1, atom_2)] = distance
            
            elapsed_time = time.time() - start_time
            click.echo(style(f"Processed {filename} with {num_of_atoms} atoms in {round(elapsed_time, 2)}s\n", fg="blue"))

            # Append a row to the log csv file
            data = {
                "CIF file": filename,
                "Number of atoms in supercell": num_of_atoms,
                "Processing time (s)": round(elapsed_time, 3)
            }
            results.append(data)
        
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

    adjusted_unique_pairs_distances = bond.strip_labels_and_remove_duplicate_atom_type_pairs(unique_pairs_distances)
    
    # Extract all unique elements from the pairs
    unique_elements = list(set([element for pair in adjusted_unique_pairs_distances.keys() for element in pair]))

    # Generate all possible pairs (with ordering matter)
    all_possible_pairs = list(permutations(unique_elements, 2))

    # Make sure each pair is sorted
    all_possible_pairs = [tuple(sorted(pair)) for pair in all_possible_pairs]

    # Remove duplicates after sorting
    all_possible_pairs = list(set(all_possible_pairs))

    # Sort the pairs in the data as well before comparison
    sorted_pairs_data = [tuple(sorted(pair)) for pair in adjusted_unique_pairs_distances.keys()]

    # Find the pairs that are not in the data
    missing_pairs = [pair for pair in all_possible_pairs if pair not in sorted_pairs_data]

    
    '''
    PART 4: SAVE & PLOT
    '''
    if len(cif_file_path_list) > 0:
        # Create a directory if needed
        output_directory_path = os.path.join(directory_path, "output")

        # Check if the output directory exists, create it if it does not
        if not os.path.exists(output_directory_path):
            os.makedirs(output_directory_path)
            
        adjusted_unique_pairs_distances = bond.strip_labels_and_remove_duplicate_atom_type_pairs(
            unique_pairs_distances
        )

        histogram.plot_histograms(
            unique_pairs_distances,
            directory_path
        )

        folder.write_summary_and_missing_pairs(
            adjusted_unique_pairs_distances,
            missing_pairs,
            directory_path
        )
                                    
        # Save csv
        folder.save_to_csv_directory(
            directory_path,
            pd.DataFrame(results),
            "log"
        )

        total_elapsed_time = time.time() - overall_start_time
        print(f"Total processing time for all files: {total_elapsed_time:.2f} seconds")


    '''
    PART 5: ERROR
    '''    

    if len(error_files) > 0:
        print(f'\nTotal files that caused errors: {len(error_files)}')
        # Print each file that caused an error
        for file in error_files:
            print(f'File with error: {file}')

    print("\nAll files successfully processed.")
    

if __name__ == "__main__":
    main()


