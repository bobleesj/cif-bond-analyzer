import os
from os.path import join
from cifkit import CifEnsemble
import click


def contains_cif_files(directory):
    """
    Check if directory or its nested directories contain any .cif files.
    """
    for root, dirs, files in os.walk(directory):
        if any(file.endswith(".cif") for file in files):
            return True
    return False


def get_cif_dir_names(script_path):
    """
    Return a list of directory names containing .cif files, excluding those
    starting with 'tests'. Directory names are relative to the script_path.
    """
    dir_names = [
        os.path.basename(d)
        for d in os.listdir(script_path)
        if os.path.isdir(os.path.join(script_path, d))
        and not d.startswith("tests")  # Exclude directories starting with 'tests'
        and contains_cif_files(os.path.join(script_path, d))
    ]

    if not dir_names:
        print("No directories found in the current path containing .cif files.")
        return []  # Return an empty list instead of None

    return dir_names


def get_json_dir_names(script_path):
    """
    Return .cif directories containing .json in the output folder.
    """
    directories = os.listdir(script_path)

    dir_name_list = []
    for d in directories:
        dir_path = os.path.join(script_path, d)
        if os.path.isdir(dir_path):
            output_dir_path = os.path.join(dir_path, "output")
            if os.path.exists(output_dir_path) and os.path.isdir(output_dir_path):
                files = os.listdir(output_dir_path)
                for file in files:
                    if file.endswith(".json"):
                        parent_dir_name = os.path.basename(
                            dir_path
                        )  # Get the parent directory name
                        dir_name_list.append(parent_dir_name)
                        break

    if not dir_name_list:
        print("No directories found in the current path containing JSON files!")
        return None

    return dir_name_list


def get_dir_list(ext, script_path):
    """Return directory names with .cif files."""
    matching_dir_names = [
        d
        for d in os.listdir(script_path)
        if os.path.isdir(join(script_path, d))
        and any(file.endswith(ext) for file in os.listdir(join(script_path, d)))
    ]

    if not matching_dir_names:
        print("No directories found in the current path containing .cif files!")
        return None
    return matching_dir_names


def get_dir_paths_with_two_or_three_elements_nested(script_path):
    """
    Allow the user to select a binary/ternary directory containing CIF files
    with 2 or 3 unique elements. Also include the list of these elements
    and file count.
    """
    # List all directories under the script path that contain .cif files, including nested folders
    dir_paths = get_cif_dir_names(script_path)
    biarny_ternary_dir_paths = {}
    for dir_path in dir_paths:
        cif_ensemble = CifEnsemble(dir_path, preprocess=False, add_nested_files=True, compute_CN=True)
        unique_elements_count = len(cif_ensemble.unique_elements)

        if unique_elements_count == 2 or unique_elements_count == 3:
            file_count = len(
                cif_ensemble.cifs
            )  # Assuming cif_ensemble.cifs returns a list of cif files
            biarny_ternary_dir_paths[dir_path] = {
                "element_count": unique_elements_count,
                "elements": cif_ensemble.unique_elements,
                "file_count": file_count,
            }

    return biarny_ternary_dir_paths


def choose_binary_ternary_dir(script_path):
    binary_ternary_dir_paths = get_dir_paths_with_two_or_three_elements_nested(
        script_path
    )

    # Check if there are directories available
    if not binary_ternary_dir_paths:
        print("No directories meet the criteria.")
        return

    # Print available directories
    print("\nAvailable folders containing 2 or 3 unique elements:")

    dir_path_list = list(binary_ternary_dir_paths.keys())

    for idx, dir_path in enumerate(dir_path_list, start=1):
        dir_info = binary_ternary_dir_paths[dir_path]
        element_count = dir_info["element_count"]
        elements = ", ".join(dir_info["elements"])
        file_count = dir_info["file_count"]
        print(
            f"{idx}. {dir_path}, {element_count} elements ({elements}), {file_count} files"
        )

    # Ask user to choose all or select specific folders
    print("\nWould you like to process each folder above sequentially?")
    process_all = click.confirm("(Default: Y)", default=True)
    if not process_all:
        input_str = input("\nEnter folder numbers to select (e.g., '1 3 5'): ")
        selected_indices = [int(num) for num in input_str.split() if num.isdigit()]

        selected_dir_paths = [
            dir_path_list[
                i - 1
            ]  # Access by index; user input is 1-based, list is 0-based
            for i in selected_indices
            if 1 <= i <= len(dir_path_list)
        ]

    else:
        # Automatically process all directories sequentially by default
        selected_dir_paths = dir_path_list

    print("The following folders are selected for processing:")
    for dir_path in selected_dir_paths:
        print(f"- {dir_path}")

    return selected_dir_paths


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
