import os
from preprocess import cif_parser
from preprocess import supercell
from util import folder


def get_cif_info(file_path, loop_tags, supercell_generation_method=3):
    """
    Parse CIF data from file path.
    """
    cif_block = cif_parser.get_cif_block(file_path)
    (
        cell_lengths,
        cell_angles_rad,
    ) = cif_parser.get_cell_lenghts_angles_rad(cif_block)
    cif_loop_values = cif_parser.get_loop_values(cif_block, loop_tags)
    all_coords_list = supercell.get_coords_list(
        cif_block, cif_loop_values
    )
    (
        all_points,
        unique_labels,
        atom_site_list,
    ) = supercell.get_points_and_labels(
        all_coords_list,
        cif_loop_values,
        supercell_generation_method,
    )

    return (
        cif_block,
        cell_lengths,
        cell_angles_rad,
        all_coords_list,
        all_points,
        unique_labels,
        atom_site_list,
    )


def get_cif_loop_values(file_path: str) -> list:
    """
    Get loop values from CIF file.
    """
    loop_tags = cif_parser.get_loop_tags()
    cif_block = cif_parser.get_cif_block(file_path)
    cif_loop_values = cif_parser.get_loop_values(cif_block, loop_tags)

    return cif_loop_values


def get_folder_and_files_info(
    script_directory: str, is_interactive_mode: bool
):
    """
    Get info about folders and files.
    """
    # With graphic user interface
    if is_interactive_mode:
        folder_info = folder.choose_dir(script_directory)
        folder_name = os.path.basename(folder_info)

    # No graphic user interface
    if not is_interactive_mode:
        folder_info = script_directory
        folder_name = os.path.basename(folder_info)

    filtered_folder_name = f"{folder_name}_filter_dist_min"
    filtered_folder = os.path.join(folder_info, filtered_folder_name)
    files_lst = [
        os.path.join(folder_info, file)
        for file in os.listdir(folder_info)
        if file.endswith(".cif")
    ]
    num_of_files = len(files_lst)
    loop_tags = cif_parser.get_loop_tags()

    return (
        folder_info,
        filtered_folder,
        files_lst,
        num_of_files,
        loop_tags,
    )
