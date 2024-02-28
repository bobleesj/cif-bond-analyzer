import os
import glob
import shutil
import preprocess.cif_parser as cif_parser
import util.folder as folder
import textwrap


def copy_files_based_on_atomic_occupancy_mixing(script_directory, is_interactive_mode=True):
    introductory_paragraph = textwrap.dedent("""\
    ===
    Welcome to the CIF Atomic Occupancy and Mixing Filter Tool!

    This tool reads CIF files from a specified directory and sorts them based on the atomic occupancy 
    and the presence of atomic mixing. The tool offers various filtering options:

    [1] Files with full occupancy
    [2] Files with site deficiency and atomic mixing
    [3] Files with full occupancy and atomic mixing
    [4] Files with site deficiency but no atomic mixing

    After you choose one of the above options, the files will be copied (not moved) to 
    corresponding sub-directories within the chosen folder. This allows you to maintain a 
    organized dataset for further analysis or processing.

    Let's get started!
    ===
    """)
    
    print(introductory_paragraph)
    _, chosen_folder_path, files = get_cif_files_and_folder_info(script_directory, is_interactive_mode)
    if len(files) is not None:
        process_files(files, chosen_folder_path)

    print("Finished - relevant folder(s) and file(s) moved!")


def get_cif_files_and_folder_info(script_directory, is_interactive_mode):

    if is_interactive_mode:
        chosen_folder_path = folder.choose_CIF_directory(script_directory)
        chosen_folder_name = os.path.basename(chosen_folder_path)
        if not chosen_folder_path:
            print("No directory chosen. Exiting.")
            return None, None, None, None
        
    # No graphic user interface
    if not is_interactive_mode:
        chosen_folder_path = script_directory
        chosen_folder_name = os.path.basename(chosen_folder_path)

    files = glob.glob(os.path.join(chosen_folder_path, "*.cif"))
    return chosen_folder_name, chosen_folder_path, files


def get_atom_info(CIF_loop_values, i):
    label = CIF_loop_values[0][i]
    occupancy = float(cif_parser.remove_string_braket(CIF_loop_values[7][i]))
    coordinates = (cif_parser.remove_string_braket(CIF_loop_values[4][i]),
                   cif_parser.remove_string_braket(CIF_loop_values[5][i]),
                   cif_parser.remove_string_braket(CIF_loop_values[6][i]))
    return label, occupancy, coordinates


def has_full_occupancy(CIF_loop_values, num_atom_labels):
    for i in range(num_atom_labels):
        _, occupancy, _ = get_atom_info(CIF_loop_values, i)
        if occupancy != 1:
            return False
    return True


def create_and_copy_to_directory(chosen_folder_path, folder_suffix, file):
    folder_name = os.path.basename(chosen_folder_path)
    destination_directory = os.path.join(chosen_folder_path, f"{folder_name}_{folder_suffix}")
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    shutil.copy(file, os.path.join(destination_directory, os.path.basename(file)))


def process_files(files, chosen_folder_path):
    for idx, file in enumerate(files, start=1):
        filename = os.path.basename(file)
        CIF_block = cif_parser.get_CIF_block(file)
        CIF_loop_values = cif_parser.get_loop_values(CIF_block, cif_parser.get_loop_tags())
        num_atom_labels = len(CIF_loop_values[0])

        # Check for full occupancy
        coordinate_occupancy_sum = {}
        is_full_occupancy = True

        for i in range(num_atom_labels):
            label, occupancy, coordinates = get_atom_info(CIF_loop_values, i)
            coordinate_occupancy_sum[coordinates] = coordinate_occupancy_sum.get(coordinates, 0) + occupancy

        # Now check summed occupancies
        for coordinates, sum_occ in coordinate_occupancy_sum.items():
            if sum_occ != 1:
                is_full_occupancy = False
                print(f"Summed occupancy at {coordinates}: {sum_occ}")  # Debug line
                break

        # Check for atomic mixing
        is_atomic_mixing = len(coordinate_occupancy_sum) != num_atom_labels

        print(filename)
        print("is_atomic_mixing", is_atomic_mixing)
        print("is_full_occupancy", is_full_occupancy)
        print()

        if is_atomic_mixing and not is_full_occupancy:
            create_and_copy_to_directory(chosen_folder_path, "deficiency_atomic_mixing", file)
        elif is_atomic_mixing and is_full_occupancy:
            create_and_copy_to_directory(chosen_folder_path, "full_occupancy_atomic_mixing", file)
        elif not is_atomic_mixing and not is_full_occupancy:
            create_and_copy_to_directory(chosen_folder_path, "deficiency_no_atomic_mixing", file)
        elif is_full_occupancy:
            create_and_copy_to_directory(chosen_folder_path, "full_occupancy", file)
