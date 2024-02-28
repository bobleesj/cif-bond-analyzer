import os
import pandas as pd
import glob
import util.folder as folder
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell


def preprocess_cif_file(file_path, compound_formula):
    update_cif_file = False

    with open(file_path, 'r') as f:
        content = f.read()

    CIF_block = cif_parser.get_CIF_block(file_path)
    CIF_loop_values = cif_parser.get_loop_values(CIF_block, cif_parser.get_loop_tags())
    num_element_labels = len(CIF_loop_values[0])

    if num_element_labels < 2:
        raise RuntimeError("Wrong number of values in the loop")


    for i in range(num_element_labels):
        label = CIF_loop_values[0][i]
        element = CIF_loop_values[1][i]
        original_label = label

        # Skip if label contains a comma
        if "," in label:
            continue
        
        # Check whether get_atom_type gives error
        atom_type_from_label = cif_parser.get_atom_type(label)

        if label[0].isdigit():
            label = label[1:]
            continue

        if atom_type_from_label != element:
            print("Atom in the label and the element do not match")
            if label[0].isdigit():
                label = label[1:]

            # Replace only the atom type in the label while keeping the rest of the label unchanged
            new_label = label.replace(atom_type_from_label, element)
            content = content.replace(original_label, new_label)
            update_cif_file = True

    if update_cif_file:
        with open(file_path, 'w') as f:
            f.write(content)
            
def move_files_based_on_format_error(script_directory):
    
    print("\nCIF Preprocessing has started...\n") 

    # Set the directory for input
        # Choose the directory
    directory_path = folder.choose_CIF_directory(script_directory)
    if not directory_path:
        print("No directory chosen. Exiting.")
        return
    
    chosen_directory_name = os.path.basename(directory_path)

    # Define the directory paths for different error types
    CIF_directory_path_bad_CIF = os.path.join(directory_path, f"{chosen_directory_name}_error_format")
    CIF_directory_path_bad_op = os.path.join(directory_path, f"{chosen_directory_name}_error_op")
    CIF_directory_path_bad_coords = os.path.join(directory_path, f"{chosen_directory_name}_error_coords")
    CIF_directory_path_bad_label = os.path.join(directory_path, f"{chosen_directory_name}_error_label")
    CIF_directory_path_bad_third_line = os.path.join(directory_path, f"{chosen_directory_name}_error_third_line")
    CIF_directory_path_bad_other_error = os.path.join(directory_path, f"{chosen_directory_name}_error_others")

    # Initialize counters for each error directory
    num_files_bad_op = 0
    num_files_bad_CIF = 0
    num_files_bad_coords = 0
    num_files_bad_label = 0
    num_files_bad_third_line = 0
    num_files_bad_others = 0
    
    # Get the list of all CIF files in the directory
    files = glob.glob(os.path.join(directory_path, "*.cif"))
    total_files = len(files)
    file_errors = []

    for idx, file_path in enumerate(files, start=1):  # Use enumerate to get the index
        filename = os.path.basename(file_path)


        try:
            result = cif_parser.get_compound_phase_tag_id_from_third_line(file_path)
            _, compound_formula, _, _ = result
            preprocess_cif_file(file_path, compound_formula)
            print(f"Processing {filename} ({idx} out of {total_files})")

            CIF_block = cif_parser.get_CIF_block(file_path)
            CIF_loop_values = cif_parser.get_loop_values(CIF_block, cif_parser.get_loop_tags())
            all_coords_list = supercell.get_coords_list(CIF_block, CIF_loop_values)
            _, _, _ = supercell.get_points_and_labels(all_coords_list, CIF_loop_values)
            

        except Exception as e:
            error_message = str(e)
            print(error_message)

            # Append file and error details to the list
            file_errors.append({
                'filename': file_path,
                'error_message': error_message
            })

            if 'An error occurred while processing symmetry operation' in error_message:
                os.makedirs(CIF_directory_path_bad_op, exist_ok=True) 
                debug_filename = os.path.join(CIF_directory_path_bad_op, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_op += 1
            elif 'Wrong number of values in the loop' in error_message:
                os.makedirs(CIF_directory_path_bad_CIF, exist_ok=True)
                debug_filename = os.path.join(CIF_directory_path_bad_CIF, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_CIF += 1
            elif 'Missing atomic coordinates' in error_message:
                os.makedirs(CIF_directory_path_bad_coords, exist_ok=True)
                debug_filename = os.path.join(CIF_directory_path_bad_coords, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_coords += 1
            elif 'Different elements found in atom site and label' in error_message:
                os.makedirs(CIF_directory_path_bad_label, exist_ok=True)
                debug_filename = os.path.join(CIF_directory_path_bad_label, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_label += 1
            elif 'The CIF file is wrongly formatted in the third line' in error_message:
                os.makedirs(CIF_directory_path_bad_third_line, exist_ok=True)
                debug_filename = os.path.join(CIF_directory_path_bad_third_line, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_third_line += 1
            else:
                os.makedirs(CIF_directory_path_bad_other_error, exist_ok=True)
                debug_filename = os.path.join(CIF_directory_path_bad_other_error, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_others += 1
            print()
    
    # Display the number of files moved to each folder
    print("\nSUMMARY")
    print(f"Number of files moved to 'error_op' folder: {num_files_bad_op}")
    print(f"Number of files moved to 'error_format' folder: {num_files_bad_CIF}")
    print(f"Number of files moved to 'error_coords' folder: {num_files_bad_coords}")
    print(f"Number of files moved to 'error_label' folder: {num_files_bad_label}")
    print(f"Number of files moved to 'error_third_line' folder: {num_files_bad_third_line}")
    print(f"Number of files moved to 'error_others' folder: {num_files_bad_others}")
    
    df_errors = pd.DataFrame(file_errors)

    # Use the save_to_csv_directory function to save the DataFrame
    folder.save_to_csv_directory(directory_path, df_errors, "error_log")