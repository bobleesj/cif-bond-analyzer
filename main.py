import os
import time
import pandas as pd
from click import style, echo

import preprocess.cif_parser as cif_parser
import preprocess.cif_parser_handler as cif_parser_handler
import preprocess.supercell as supercell
import postprocess.bond as bond
import postprocess.histogram as histogram
import util.folder as folder
import util.prompt as prompt

def main():
    prompt.print_intro_prompt()

    '''
    PART 1: Choose the folder & get user input
    '''

    error_files = []  # list to hold names of files that cause an error
    global_pairs_data = {}
    log_list = []

    script_directory = os.path.dirname(os.path.abspath(__file__))
    directory_path = folder.choose_CIF_directory(script_directory)
    cif_file_path_list = folder.get_cif_file_path_list_from_directory(directory_path)
    supercell_generation_method_above_200_atoms = prompt.get_user_input_on_supercell_generation_method()

    # If the user chooses no option, then it's simply 3
    if not supercell_generation_method_above_200_atoms:
        print("\nYour default option is generating a 2-2-2 supercell for files with more than 200 atoms in the unit cell.")
        supercell_generation_method_above_200_atoms = 3

    '''
    PART 2: PREPROCESS
    '''

    # For each file in the list of files
    for i, cif_file_path in enumerate(cif_file_path_list):
        
        # For each file
        start_time = time.time()
        overall_start_time = time.time()
        filename = os.path.basename(cif_file_path)      
        num_of_atoms = None      

        try:
            # Process CIF files and return a list of coordinates after applying symmetry operations
            _, cell_lengths, cell_angles_rad, _,all_points, _, atom_site_list = cif_parser_handler.get_CIF_info(
                cif_file_path,
                cif_parser.get_loop_tags(),
                supercell_generation_method_above_200_atoms
                )

            num_of_atoms = len(all_points)
            echo(style(f"Processing {filename} with {num_of_atoms} atoms ({i+1}/{len(cif_file_path_list)})", fg="black"))
            atomic_pair_list = supercell.get_atomic_pair_list(all_points, cell_lengths, cell_angles_rad)

            if folder.get_file_type(atom_site_list) in ["binary", "ternary", "quaternary"]:
                processed_pairs_ordered = bond.process_and_order_pairs(all_points, atomic_pair_list)
                unique_pairs_dict = {}

                for pair in processed_pairs_ordered:

                    atom_label_0 = pair["labels"][0]
                    atom_label_1 = pair["labels"][1]

                    # Create a tuple of the labels
                    labels_tuple = (atom_label_0, atom_label_1)

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
                        # atom_1 = cif_parser.get_atom_type(labels[0])
                        # atom_2 = cif_parser.get_atom_type(labels[1])
                        atom_1 = labels[0]
                        atom_2 = labels[1]
                        distance = str(round(pair['distance'], 3)).ljust(5)
                        print(f"Pair: {atom_1}-{atom_2} {distance} Å")
                        # Store to the global overview dataset
                        global_pairs_data[filename][(atom_1, atom_2)] = distance
            
            elapsed_time = time.time() - start_time
            echo(style(f"Processed {filename} with {num_of_atoms} atoms in {round(elapsed_time, 2)}s\n", fg="blue"))

            # Append a row to the log csv file
            data = {
                "CIF file": filename,
                "Number of atoms in supercell": num_of_atoms,
                "Processing time (s)": round(elapsed_time, 3)
            }
            log_list.append(data)
        
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
    missing_pairs = bond.get_missing_pairs(adjusted_unique_pairs_distances)

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

        folder.write_summary_and_missing_pairs(
            adjusted_unique_pairs_distances,
            missing_pairs,
            directory_path
        )

        histogram.plot_histograms(
            unique_pairs_distances,
            directory_path
        )
                            
        # Save csv
        folder.save_to_csv_directory(
            directory_path,
            pd.DataFrame(log_list),
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


