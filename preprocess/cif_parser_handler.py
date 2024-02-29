import preprocess.supercell as supercell
import preprocess.cif_parser as cif_parser
import os
import click
from click import style
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import util.folder as folder


def get_CIF_info(file_path, loop_tags):
    """
    Parse the CIF data from the given file path.
    """
    CIF_block = cif_parser.get_CIF_block(file_path)
    cell_lengths, cell_angles_rad = cif_parser.get_cell_lenghts_angles_rad(CIF_block)
    CIF_loop_values = cif_parser.get_loop_values(CIF_block, loop_tags)
    all_coords_list = supercell.get_coords_list(CIF_block, CIF_loop_values)
    all_points, unique_labels, unique_atoms_tuple = supercell.get_points_and_labels(all_coords_list, CIF_loop_values)
    
    return CIF_block, cell_lengths, cell_angles_rad, all_coords_list,all_points, unique_labels, unique_atoms_tuple


def get_folder_and_files_info(script_directory, isInteractiveMode):
    print("script_directory", script_directory)
    """
    Get the folder information, list of CIF files, and loop tags for processing.
    
    Parameters:
    - script_directory: The base directory from which to select the CIF directory.
    
    Returns:
    - folder_info: Information about the selected folder.
    - filtered_folder: Path to the folder where filtered files will be stored.
    - files_lst: List of CIF files to process.
    - num_of_files: Number of CIF files found.
    - loop_tags: Loop tags used for parsing CIF files.
    """

    # With graphic user interface
    if isInteractiveMode:
        folder_info = folder.choose_CIF_directory(script_directory)
        folder_name = os.path.basename(folder_info)
        
    # No graphic user interface
    if not isInteractiveMode:
        folder_info = script_directory
        folder_name = os.path.basename(folder_info)

    filtered_folder_name = f"{folder_name}_filter_dist_min"
    filtered_folder = os.path.join(folder_info, filtered_folder_name)
    files_lst = [os.path.join(folder_info, file) for file in os.listdir(folder_info) if file.endswith('.cif')]
    num_of_files = len(files_lst)
    loop_tags = cif_parser.get_loop_tags()
    
    return folder_info, filtered_folder, files_lst, num_of_files, loop_tags