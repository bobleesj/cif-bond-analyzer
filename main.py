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
import postprocess.pair_order as pair_order
import filter.occupancy as occupancy
import postprocess.excel as excel


def main(is_iteractive_mode=True, dir_path=None):
    prompt.print_intro_prompt()

    '''
    PART 1: Choose the folder & get user input
    '''

    error_files = []
    log_list = []
    file_path_list = None

    if is_iteractive_mode:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        dir_path = folder.choose_CIF_directory(script_directory)
        supercell_method_large_cif = prompt.get_user_input_on_supercell_method()
    
        # If the user chooses no option, then it's simply 3
        if not supercell_method_large_cif:
            print("\nYour default option is generating a 2-2-2 supercell for",
                "files more than 100 atoms in the unit cell.")
            supercell_method_large_cif = 1

    if not is_iteractive_mode:
        file_path_list = folder.get_cif_file_path_list(dir_path)
        supercell_method_large_cif = 1

    file_path_list = folder.get_cif_file_path_list(dir_path)

    '''
    PART 2: PREPROCESS
    '''
    
    dist_mixing_file_per_pair_dict = {}

    overall_start_time = time.perf_counter()
    # For each file in the list of files
    for i, file_path in enumerate(file_path_list):
        start_time = time.perf_counter()
        filename_with_ext = os.path.basename(file_path)
        filename, ext = os.path.splitext(filename_with_ext)
        num_of_atoms = None
    
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

        # Add atom_site_info to the file name
        
        
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
        
        # Save to the global pair data
        for filename, pairs in unique_pairs_dict.items():
            
            for labels, pair in pairs.items():
                pair_tuple_ordered = pair_order.order_pair_by_mendeleev(
                    (labels[0], labels[1])
                )
                label_1 = pair_tuple_ordered[0]
                label_2 = pair_tuple_ordered[1]
                dist = round(pair['distance'], 3)
                dist_str = str(dist)

                # Convert dist back to float for comparison
            
                pair_key = f"{label_1}-{label_2}"
                pair_mixing_category = label_pair_mixing_dict[pair_tuple_ordered]
                
                # Initialize pair_key if not exists
                if pair_key not in dist_mixing_file_per_pair_dict:
                    dist_mixing_file_per_pair_dict[pair_key] = {}
                
                # Check if the file is already associated with the pair_key
                if filename in dist_mixing_file_per_pair_dict[pair_key]:
                    # Update only if the new distance is shorter
                    if dist < float(dist_mixing_file_per_pair_dict[pair_key][filename]["dist"]):
                        dist_mixing_file_per_pair_dict[pair_key][filename] = {
                            "mixing": pair_mixing_category,
                            "dist": dist_str
                        }
                else:
                    # If the file is not associated yet, add it directly
                    dist_mixing_file_per_pair_dict[pair_key][filename] = {
                        "mixing": pair_mixing_category,
                        "dist": dist_str
                    }
                    
        elapsed_time = time.perf_counter() - start_time

        prompt.print_dict_in_json(dist_mixing_file_per_pair_dict)
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

    # except Exception as e:
    #     print(f'Error processing file {filename}: {e}')
    #     error_files.append(filename)

    '''
    PART 3: OUTPUT
    '''

    # print("\nlabel_pair_mixing_dict")
    # print(label_pair_mixing_dict)
    
    # # Find the unique pairs and its count across all files
    # unique_pairs_distances = bond.get_unique_pairs_distances(global_pairs_data)
    
    # print('\nunique_pairs_distances', unique_pairs_distances)

    # pair_tuples, missing_pair_tuples = bond.get_sorted_missing_pairs(
    #     unique_pairs_distances
    # )

    '''
    # PART 4: SAVE & PLOT
    # '''

    # if len(file_path_list) > 0:
    #     # Create a directory if needed
    #     output_directory_path = os.path.join(dir_path, "output")

    #     # Check if the output directory exists, create it if it does not
    #     if not os.path.exists(output_directory_path):
    #         os.makedirs(output_directory_path)

    #     adjusted_pairs_distances = bond.strip_labels_and_remove_duplicate(
    #         unique_pairs_distances
    #     )

    #     sorted_pairs_by_count = sorted(
    #         adjusted_pairs_distances.items(),
    #         key=lambda item: (len(item[1]), item[0]),
    #         reverse=True
    #     )

    #     sorted_pairs_by_count_dict = dict(sorted_pairs_by_count)

    #     folder.write_summary_and_missing_pairs(
    #         sorted_pairs_by_count_dict,
    #         missing_pair_tuples,
    #         dir_path
    #     )

    #     folder.save_to_csv_directory(
    #         dir_path,
    #         pd.DataFrame(log_list),
    #         "log"
    #     )

    #     json_data = excel.write_excel_json(
    #         dir_path,
    #         pair_tuples,
    #         global_pairs_data
    #     )

    #     histogram.plot_histograms_from_data(json_data, dir_path)

    #     total_elapsed_time = time.perf_counter() - overall_start_time
    #     print(f"Total processing time: {total_elapsed_time:.2f}s")


    # if len(error_files) > 0:
    #     print(f'\nTotal files that caused errors: {len(error_files)}')
    #     # Print each file that caused an error
    #     for file in error_files:
    #         print(f'File with error: {file}')

    print("\nAll files successfully processed.")


if __name__ == "__main__":
    main()
