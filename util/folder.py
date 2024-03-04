import os
import glob
from os.path import join, exists
from shutil import rmtree, move


def choose_CIF_directory(script_directory):
    """
    Allows the user to select a directory from the given path.
    """
    directories = [d for d in os.listdir(script_directory) 
                   if os.path.isdir(join(script_directory, d)) 
                   and any(file.endswith('.cif') for file in os.listdir(join(script_directory, d)))]
    
    if not directories:
        print("No directories found in the current path containing .cif files!")
        return None
    print("\nAvailable folders containing CIF files:")
    for idx, dir_name in enumerate(directories, start=1):
        num_of_cif_files = get_cif_file_count_from_directory(dir_name)
        print(f"{idx}. {dir_name}, {num_of_cif_files} files")
    while True:
        try:
            choice = int(input("\nEnter the number corresponding to the folder containing .cif files: "))
            if 1 <= choice <= len(directories):
                return join(script_directory, directories[choice-1])
            else:
                print(f"Please enter a number between 1 and {len(directories)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def save_to_csv_directory(folder_info, df, base_filename):
    """
    Saves the dataframe as a CSV inside a 'csv' sub-directory of the provided folder.
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
    return glob.glob(os.path.join(directory, "*.cif"))


def remove_directories(directory_list):
    for direcotry in directory_list:
        if exists(direcotry):
            rmtree(direcotry)


def move_files(to_directory, file_path_list):
    for file_path in file_path_list:
        move(file_path, to_directory)


def remove_file(file_path):
    if exists(file_path):
        os.remove(file_path)


def write_summary_and_missing_pairs(unique_pairs_distances, missing_pairs, directory_path):
    """
    Writes a summary of unique atomic pairs, including counts and distances,
    and a list of missing pairs to a file.

    Parameters:
    - unique_pairs_distances: A dictionary with atomic pairs as keys and lists of distances as values.
    - missing_pairs: A list of tuples representing missing atomic pairs.
    - directory_path: The path to the directory where the summary file will be saved.
    """

    file_path = os.path.join(directory_path, "output", "summary_and_missing_pairs.txt")
    with open(file_path, 'w') as file:
        print("Summary:")
        file.write("Summary:\n")
        for pair, distances in unique_pairs_distances.items():
            atom_1 = pair[0].strip()
            atom_2 = pair[1].strip()
            count = len(distances)
            distances_str = ''.join([f"{round(float(dist), 3):6.3f}" for dist in distances])
            file.write(f"Pair: {atom_1}-{atom_2}, Count: {count}, Distances:{distances_str}\n")
            print(f"Pair: {atom_1}-{atom_2}, Count: {count}, Distances:{distances_str}")

        print("\nMissing pairs:")
        file.write("\nMissing pairs:\n")
        for pair in missing_pairs:
            atom_1 = pair[0].strip()
            atom_2 = pair[1].strip()
            file.write(f"{atom_1}-{atom_2}\n")
            print((f"{atom_1}-{atom_2}"))

    print(f"\nSummary and missing pairs saved to {file_path}")


def get_file_type(atom_site_list):
    file_type_map = {2: "binary", 3: "ternary", 4: "quaternary"}
    unique_atom_count = len(set(atom_site_list))
    return file_type_map.get(unique_atom_count, "other")
