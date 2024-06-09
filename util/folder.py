import os
import glob
import click
from os.path import join, exists
from shutil import rmtree, move
from preprocess import cif_parser, cif_parser_handler
from util import folder


def get_cif_dir_names(script_path):
    """
    Returns a list of directories containing .cif files.
    """
    dir_name_list = [
        d
        for d in os.listdir(script_path)
        if os.path.isdir(join(script_path, d))
        and any(
            file.endswith(".cif") for file in os.listdir(join(script_path, d))
        )
    ]

    if not dir_name_list:
        print(
            "No directories found in the current path containing .cif files!"
        )
        return None

    return dir_name_list


def get_json_dir_names(script_path):
    """
    Returns .cif directories containing .json in the output folder.
    """
    directories = os.listdir(script_path)

    dir_name_list = []
    for d in directories:
        dir_path = os.path.join(script_path, d)
        if os.path.isdir(dir_path):
            output_dir_path = os.path.join(dir_path, "output")
            if os.path.exists(output_dir_path) and os.path.isdir(
                output_dir_path
            ):
                files = os.listdir(output_dir_path)
                for file in files:
                    if file.endswith(".json"):
                        parent_dir_name = os.path.basename(
                            dir_path
                        )  # Get the parent directory name
                        dir_name_list.append(parent_dir_name)
                        break

    if not dir_name_list:
        print(
            "No directories found in the current path containing JSON files!"
        )
        return None

    return dir_name_list


def get_dir_list(ext, script_path):
    """Returns directory names with .cif files."""
    matching_dir_names = [
        d
        for d in os.listdir(script_path)
        if os.path.isdir(join(script_path, d))
        and any(
            file.endswith(ext) for file in os.listdir(join(script_path, d))
        )
    ]

    if not matching_dir_names:
        print(
            "No directories found in the current path containing .cif files!"
        )
        return None
    return matching_dir_names


def choose_binary_ternary_dir(script_path, ext=".cif"):
    """
    Allows the user to select a binary/ternary directory containing CIF files
    with 2 or 3 unique elements.
    """
    # Assuming get_binary_ternary_combined_cif_dir_list is fixed to return the list of directories
    unique_element_count_per_dir = (
        folder.get_binary_ternary_combined_cif_dir_list(script_path)
    )

    # Check if there are directories available
    if not unique_element_count_per_dir:
        print("No directories meet the criteria.")
        return None
    # Print available directories
    print(
        "\nAvailable folders containing 2 or 3 unique elements across all CIF files:"
    )
    for index, (folder_name, unique_elements, file_count) in enumerate(
        unique_element_count_per_dir, start=1
    ):
        print(
            f"{index}. {folder_name} - {unique_elements} elements, {file_count} files"
        )

    # Ask user to choose all or select specific folders
    click.echo("\nWould you like to process each folder above sequentially?")
    process_all = click.confirm("(Default: Y)", default=True)
    if not process_all:
        # Interactive selection of directory if user does not want all directories
        input_str = input("\nEnter folder numbers to select (e.g., '1 3 5'): ")
        selected_dirs = []

        # Process the input string
        elements = input_str.split(" ")
        for element in elements:
            selected_dirs.append(int(element))

        selected_dir_paths = []
        for choice in selected_dirs:
            if 1 <= choice <= len(unique_element_count_per_dir):
                selected_dir = unique_element_count_per_dir[choice - 1][0]
                selected_dir_path = os.path.join(script_path, selected_dir)
                selected_dir_paths.append(selected_dir_path)
                print(f"Selected: {selected_dir}")
            else:
                print(
                    f"Invalid choice: {choice}. Please choose a number between 1 and {len(unique_element_count_per_dir)}."
                )
    else:
        # Automatically process all directories sequentially if the user accepts the default
        selected_dir_paths = [
            os.path.join(script_path, dir_info[0])
            for dir_info in unique_element_count_per_dir
        ]
        for dir_path in selected_dir_paths:
            print(f"Selected for processing: {dir_path}")

    return selected_dir_paths


# Example usage (make sure to define `script_path` and import the necessary modules in your working environment)


def choose_dir(script_path, ext=".cif"):
    """
    Allows the user to select a directory from the given path.
    """
    dir_names = get_dir_list(ext, script_path)

    print("\nAvailable folders containing CIF files:")
    for idx, dir_name in enumerate(dir_names, start=1):
        num_of_cif_files = get_cif_file_count_from_directory(dir_name)
        print(f"{idx}. {dir_name}, {num_of_cif_files} files")
    while True:
        try:
            choice = int(input("\nEnter folder # having .cif files: "))
            if 1 <= choice <= len(dir_names):
                return join(script_path, dir_names[choice - 1])
            else:
                print(f"Please enter a number between 1 and {len(dir_names)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def save_to_csv_directory(folder_info, df, base_filename):
    """
    Saves the dataframe as a CSV inside a 'csv' sub-directory.
    """
    # Create the sub-directory for CSVs if it doesn't exist

    csv_directory = join(folder_info, "csv")
    if not os.path.exists(csv_directory):
        os.mkdir(csv_directory)

    # Extract the name of the chosen folder
    folder_name = os.path.basename(folder_info)

    # Set the name for the CSV file based on the chosen folder
    csv_filename = f"{folder_name}_{base_filename}.csv"

    # Save the DataFrame to the desired location (within the 'csv' sub-directory)
    df.to_csv(join(csv_directory, csv_filename), index=False)

    print(csv_filename, "saved")


def get_cif_file_count_from_directory(directory):
    """
    Counts .cif files in a given directory.
    """
    return len(glob.glob(join(directory, "*.cif")))


def get_file_path_list(directory, ext="*.cif"):
    """
    Lists all files in the chosen folder
    """
    return glob.glob(os.path.join(directory, ext))


def remove_directories(directory_list):
    """
    Removes all files in the given directories.
    """
    for direcotry in directory_list:
        if exists(direcotry):
            rmtree(direcotry)


def move_files(to_directory, file_path_list):
    """
    Moves files to another folder.
    """
    for file_path in file_path_list:
        move(file_path, to_directory)


def remove_file(file_path):
    """
    Removes a single file.
    """
    if exists(file_path):
        os.remove(file_path)


def create_output_folder_for_neighbor(
    dir_path, radius, is_coordination_num_used
):
    """
    Creates an output folder for atomic for atomic environment info.
    """
    output_folder_path = os.path.join(dir_path, "output")

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    nested_folder_name = None
    # Define and create the nested folder based on the cutoff radius
    if is_coordination_num_used:
        nested_folder_name = "shortest_dist_CN"
    else:
        nested_folder_name = f"shortest_dist_cutoff_{radius}"

    nested_folder_path = os.path.join(output_folder_path, nested_folder_name)

    if not os.path.exists(nested_folder_path):
        os.makedirs(nested_folder_path)

    return nested_folder_path


def create_folder_under_output_dir(dir_path, folder_name):
    """
    Creates a folder inside the output folder.
    """
    # Define the path to the 'output' directory
    output_dir = join(dir_path, "output")

    # Create the 'output' directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Define the path to the 'system_analysis' director
    nested_output_dir = join(output_dir, folder_name)

    # Create the 'system_analysis' directory if it doesn't exist
    if not os.path.exists(nested_output_dir):
        os.mkdir(nested_output_dir)

    return nested_output_dir


def get_binary_ternary_combined_cif_dir_list(script_path, ext=".cif"):
    """
    Returns a list of tuples containing directory name, number of unique
    elements, and file count
    """
    # Use the script path to list folders that contain .cif files
    dir_names = get_dir_list(ext, script_path)
    unique_element_count_per_dir = []

    for dir_name in dir_names:
        cif_dir = os.path.join(script_path, dir_name)
        file_count = get_cif_file_count_from_directory(cif_dir)
        file_path_list = get_file_path_list(cif_dir, ext="*.cif")
        atom_set = set()

        # Loop each cif file in the dir
        for file_path in file_path_list:
            (
                _,
                _,
                _,
                _,
                _,
                unique_labels,
                _,
            ) = cif_parser_handler.get_cif_info(file_path)

            for label in unique_labels:
                atom = cif_parser.get_atom_type(label)
                atom_set.add(atom)
                # Check if atom set size exceeds 3
                if len(atom_set) > 3:
                    break

            if len(atom_set) > 3:
                break

        # Append only if atom set size is 2 or 3
        if len(atom_set) <= 3 and len(atom_set) > 1:
            unique_element_count_per_dir.append(
                (dir_name, len(atom_set), file_count)
            )

    return unique_element_count_per_dir


def check_whether_file_exists(file_path):
    """
    Checks if a file exists at the specified path.
    """
    return os.path.exists(file_path)
