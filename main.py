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
import filter.occupancy as occupancy


def main():
    prompt.print_intro_prompt()

    '''
    PART 1: Choose the folder & get user input
    '''

    error_files = []  # list to hold names of files that cause an error
    global_pairs_data = {}
    log_list = []

    script_directory = os.path.dirname(os.path.abspath(__file__))
    dir_path = folder.choose_CIF_directory(script_directory)
    file_path_list = folder.get_cif_file_path_list(dir_path)
    supercell_method_large_cif = prompt.get_user_input_on_supercell_method()

    # If the user chooses no option, then it's simply 3
    if not supercell_method_large_cif:
        print("\nYour default option is generating a 2-2-2 supercell for files"
              "more than 200 atoms in the unit cell.")
        supercell_method_large_cif = 3

    '''
    PART 2: PREPROCESS
    '''

    overall_start_time = time.perf_counter()
    # For each file in the list of files
    for i, file_path in enumerate(file_path_list):
        start_time = time.perf_counter()
        filename = os.path.basename(file_path)
        num_of_atoms = None

        try:
            # Process CIF files and return a list of coordinates
            result = cif_parser_handler.get_CIF_info(
                file_path,
                cif_parser.get_loop_tags(),
                supercell_method_large_cif
            )

            CIF_loop_values = cif_parser_handler.get_CIF_loop_values(
                file_path
            )

            _, lenghts, angles_rad, _, all_points, _, atom_site_list = result

            num_of_atoms = len(all_points)
            index = f"({i+1}/{len(file_path_list)})"
            msg = f"Processing {filename} with {num_of_atoms} atoms {index}"
            echo(style(msg, fg="black"))
            atomic_pair_list = supercell.get_atomic_pair_list(
                all_points,
                lenghts,
                angles_rad
            )

            occupancy.get_atom_site_mixing_info(filename, CIF_loop_values)

            file_types = ["binary", "ternary", "quaternary"]
            if folder.get_file_type(atom_site_list) in file_types:

                processed_pairs_ordered = bond.process_and_order_pairs(
                    all_points,
                    atomic_pair_list
                )

                unique_pairs_dict = {}

                for pair in processed_pairs_ordered:

                    atom_label_0 = pair["labels"][0]
                    atom_label_1 = pair["labels"][1]

                    # Create a tuple of the labels
                    label_tuple = (atom_label_0, atom_label_1)

                    # Initialize a new dictionary for this filename
                    if filename not in unique_pairs_dict:
                        unique_pairs_dict[filename] = {}

                    # If these labels have not been seen before or
                    # if this pair is shorter than the previous pair
                    if (label_tuple not in unique_pairs_dict[filename] or
                        pair["distance"] < unique_pairs_dict[filename][label_tuple]["distance"]):

                        # Add this pair to the dictionary
                        unique_pairs_dict[filename][label_tuple] = pair
    
                # Sort the pair alphabetically
                for filename, pairs in unique_pairs_dict.items():
                    global_pairs_data[filename] = {}
                    # print("*Print all pairs with labels for debugging.")
                    print("*Only unique shortest pairs recorded to .txt")
                    for labels, pair in pairs.items():
                        atom_1, atom_2 = sorted(
                            [cif_parser.get_atom_type(labels[0]),
                             cif_parser.get_atom_type(labels[1])]
                        )
                        dist = str(round(pair['distance'], 3))
                        print(f"Pair: {atom_1}-{atom_2} {dist} Å")
                        # Store to the global overview dataset
                        global_pairs_data[filename][(atom_1, atom_2)] = dist
 
            elapsed_time = time.perf_counter() - start_time
            echo(style(f"Processed {filename} with {num_of_atoms} atoms in {round(elapsed_time, 2)} s\n", fg="blue"))

            # Append a row to the log csv file
            data = {
                "CIF file": filename,
                "Number of atoms in supercell": num_of_atoms,
                "Processing time (s)": round(elapsed_time, 3)
            }
            log_list.append(data)
        
        except Exception as e:
            print(f'Error processing file {filename}: {e}')
            error_files.append(filename)

    print(global_pairs_data)
    # Find the unique pairs and its count across all files
    unique_pairs_distances = {}
    for filename, pairs in global_pairs_data.items():
        for pair, dist in pairs.items():
            if pair not in unique_pairs_distances:
                unique_pairs_distances[pair] = [dist]
            else:
                unique_pairs_distances[pair].append(dist)

    '''
    PART 3: OUTPUT
    '''

    adjusted_pairs_distances = bond.strip_labels_and_remove_duplicate(
        unique_pairs_distances
    )
    unique_pair_tuple_list, missing_pair_tuple_list = bond.get_sorted_missing_pairs(
        adjusted_pairs_distances
    )

    # Initialize a dictionary to hold the pairs and the .cif files
    pairs_files_mapping = {}

    for pair in unique_pair_tuple_list:
        pairs_files_mapping[pair] = []
        for filename, pairs in global_pairs_data.items():
            # If the pair is present in the cif file
            if pair in pairs:
                pairs_files_mapping[pair].append(filename)

    # Print the mapping of pairs to files
    for pair, files in pairs_files_mapping.items():
        print(f"Pair {pair} is found in: {files}")

    # Create a Pandas Excel writer using openpyxl as the engine
    excel_writer = pd.ExcelWriter("unique_pairs.xlsx", engine='openpyxl')

    # Iterate over each unique pair
    for pair, files in pairs_files_mapping.items():
        # Initialize a list to hold the data for this pair
        data_for_pair = []
        
        # For each file that contains this pair, add the filename and dist
        for file in files:
            distance = float(global_pairs_data[file][pair])
            data_for_pair.append({'File': file, 'Distance': distance})
        
        # Convert the list to a DataFrame
        df = pd.DataFrame(data_for_pair)
        
        # Write the DataFrame to a sheet named after the pair
        sheet_name = f"{pair[0]}-{pair[1]}"
        df.to_excel(excel_writer, sheet_name=sheet_name, index=False)

    # Save the Excel file
    excel_writer.close()

    '''
    PART 4: SAVE & PLOT
    '''

    if len(file_path_list) > 0:
        # Create a directory if needed
        output_directory_path = os.path.join(dir_path, "output")

        # Check if the output directory exists, create it if it does not
        if not os.path.exists(output_directory_path):
            os.makedirs(output_directory_path)

        adjusted_pairs_distances = bond.strip_labels_and_remove_duplicate(
            unique_pairs_distances
        )

        folder.write_summary_and_missing_pairs(
            adjusted_pairs_distances,
            missing_pair_tuple_list,
            dir_path
        )

        histogram.plot_histograms(
            adjusted_pairs_distances,
            dir_path
        )

        folder.save_to_csv_directory(
            dir_path,
            pd.DataFrame(log_list),
            "log"
        )

        total_elapsed_time = time.perf_counter() - overall_start_time
        print(f"Total processing time: {total_elapsed_time:.2f}s")

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
