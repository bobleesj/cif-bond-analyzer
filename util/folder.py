import os
import glob
from os.path import join, exists
from shutil import rmtree, move


def get_cif_dir_names(script_path):
    dir_name_list = [
        d
        for d in os.listdir(script_path)
        if os.path.isdir(join(script_path, d))
        and any(
            file.endswith(".cif")
            for file in os.listdir(join(script_path, d))
        )
    ]

    if not dir_name_list:
        print(
            "No directories found in the current path containing .cif files!"
        )
        return None

    return dir_name_list


def get_json_dir_names(script_path):
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
                        break  # Found a JSON file, no need to check further in this directory

    if not dir_name_list:
        print(
            "No directories found in the current path containing JSON files!"
        )
        return None

    return dir_name_list


def choose_cif_dir(script_path):
    """
    Allows the user to select a directory from the given path.
    """
    directories = [
        d
        for d in os.listdir(script_path)
        if os.path.isdir(join(script_path, d))
        and any(
            file.endswith(".cif")
            for file in os.listdir(join(script_path, d))
        )
    ]

    if not directories:
        print(
            "No directories found in the current path containing .cif files!"
        )
        return None
    print("\nAvailable folders containing CIF files:")
    for idx, dir_name in enumerate(directories, start=1):
        num_of_cif_files = get_cif_file_count_from_directory(dir_name)
        print(f"{idx}. {dir_name}, {num_of_cif_files} files")
    while True:
        try:
            choice = int(
                input("\nEnter folder # having .cif files: ")
            )
            if 1 <= choice <= len(directories):
                return join(script_path, directories[choice - 1])
            else:
                print(
                    f"Please enter a number between 1 and {len(directories)}."
                )
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
    """Helper function to count .cif files in a given directory."""
    return len(glob.glob(join(directory, "*.cif")))


def get_cif_file_path_list(directory):
    """Get all file path list from folde."""
    return glob.glob(os.path.join(directory, "*.cif"))


def remove_directories(directory_list):
    """Remove all files given directories."""
    for direcotry in directory_list:
        if exists(direcotry):
            rmtree(direcotry)


def move_files(to_directory, file_path_list):
    """Move files to a folder."""
    for file_path in file_path_list:
        move(file_path, to_directory)


def remove_file(file_path):
    """Remove a single file."""
    if exists(file_path):
        os.remove(file_path)


def create_output_folder_for_neighbor(dir_path, name):
    output_folder_path = os.path.join(dir_path, "output")

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Define and create the nested folder based on the cutoff radius
    nested_folder_name = f"shortest_dist_cutoff_{name}"
    nested_folder_path = os.path.join(
        output_folder_path, nested_folder_name
    )

    if not os.path.exists(nested_folder_path):
        os.makedirs(nested_folder_path)

    return nested_folder_path
