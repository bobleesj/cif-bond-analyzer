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
            choice = int(input("\nEnter folder # having .cif files: "))
            if 1 <= choice <= len(directories):
                return join(script_directory, directories[choice-1])
            else:
                print(f"Please enter a number between 1 and {len(directories)}.")
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


def write_summary_and_missing_pairs(
        dist_mix_pair_dict,
        missing_pairs,
        dir_path):
    """
    Writes a summary of unique atomic pairs, including counts and distances,
    and a list of missing pairs to a file.

    Parameters:
    - unique_pairs_distances: A dictionary with atomic pairs as keys and lists.
    - missing_pairs: A list of tuples representing missing atomic pairs.
    - directory_path: The path to the directory where the summary file savde.
    """

    file_path = os.path.join(dir_path, "output", "summary.txt")

    # Step 1: Collect data
    data = []
    for pair, files in dist_mix_pair_dict.items():
        distances = sorted(float(info['dist']) for info in files.values())
        count = len(distances)
        dists = ', '.join(f"{distance:.3f}" for distance in distances)
        data.append((pair, count, dists))

    # Step 2: Sort the data first by count (descending) then by pair name
    sorted_data = sorted(data, key=lambda x: (-x[1], x[0]))

    # Step 3: Write sorted data to file
    with open(file_path, 'w') as file:
        file.write("Summary:\n")
        for pair, count, dists in sorted_data:
            file.write(f"Pair: {pair}, Count: {count} Distances: {dists}\n")

        # x[0][0] - use 1st cha of the first element
        # x[0] - use the first element to sort
        # x[1] - use the second element to sort
        print("\nMissing pairs:")
        file.write("\nMissing pairs:\n")
        missing_pairs_sorted = sorted(
            missing_pairs, key=lambda x: (x[0][0], x[0], x[1])
        )
        for pair in missing_pairs_sorted:
            atom_1 = pair[0].strip()
            atom_2 = pair[1].strip()
            file.write(f"{atom_1}-{atom_2}\n")
            print((f"{atom_1}-{atom_2}"))

    print(f"\nSummary and missing pairs saved to {file_path}")
