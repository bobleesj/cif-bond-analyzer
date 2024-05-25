"""
Determines the nearest neighbor distances from each atomic site
based on the cutoff distance provided

Author: Sangjoon Bob Lee
Last update: May 19, 2024
Release date: Mar 10, 2024
"""

import os
import time
from preprocess import (
    cif_parser_handler,
    format,
    supercell_handler,
)
from click import echo
from util import folder, prompt
from postprocess import neighbor


def run_atomic_environment(script_path):
    dir_names_with_cif = folder.get_cif_dir_names(script_path)

    # If no folders containing .cif files found, exit
    if not dir_names_with_cif:
        return

    cutoff_radius = None
    is_cn_used = prompt.get_is_coordination_num_used()

    if not is_cn_used:
        cutoff_radius = prompt.get_cutoff_radius()
    else:
        # Default of 10. Later, connections will be filtered based on CN
        cutoff_radius = 10

    selected_dirs = prompt.get_user_input_folder_processing(
        dir_names_with_cif, ".cif"
    )

    dir_names_with_cif = folder.get_cif_dir_names(script_path)

    # If no folders containing .cif files found, exit
    if not dir_names_with_cif:
        return

    is_cn_used = True
    cutoff_radius = 10
    num_selected_dirs = len(selected_dirs)

    for idx, dir_name in enumerate(selected_dirs.values(), start=1):
        dir_path = os.path.join(script_path, dir_name)
        file_path_list = folder.get_file_path_list(dir_path)
        overall_start_time = time.perf_counter()
        prompt.echo_folder_progress(idx, dir_name, num_selected_dirs)

        # PART 1: Pre-process
        format.move_files_based_on_format_error(dir_path)
        file_path_list = folder.get_file_path_list(dir_path)

        output_folder = folder.create_output_folder_for_neighbor(
            dir_path, cutoff_radius, is_cn_used
        )

        # PART 2: Process each file
        for i, file_path in enumerate(file_path_list):
            # Dictionary to store connections for each label
            all_labels_connections = {}
            start_time = time.perf_counter()
            filename_with_ext = os.path.basename(file_path)
            filename, _ = os.path.splitext(filename_with_ext)
            result = cif_parser_handler.get_cif_info(file_path)
            (
                _,
                lengths,
                angles,
                _,
                supercell_points,
                labels,
                _,
            ) = result

            unitcell_points = (
                supercell_handler.get_flattened_points_from_unitcell(
                    file_path
                )
            )

            prompt.print_progress_current(
                i, filename_with_ext, supercell_points
            )

            # PART 3: Process each atomic label
            for site_label in labels:
                filtered_unitcell_points = [
                    point
                    for point in unitcell_points
                    if point[3] == site_label
                ]

                dist_result = neighbor.get_nearest_dists_per_site(
                    filtered_unitcell_points,
                    supercell_points,
                    cutoff_radius,
                    lengths,
                    angles,
                )

                dist_dict, dist_set = dist_result

                (
                    label,
                    connections,
                ) = neighbor.get_most_connected_point_per_site(
                    site_label, dist_dict, dist_set
                )

                all_labels_connections[label] = connections

            # Determine coordination number
            if is_cn_used:
                all_labels_connections = (
                    neighbor.filter_connections_with_CN(
                        all_labels_connections
                    )
                )

            all_labels_connections = neighbor.add_diff_after(
                all_labels_connections
            )

            # neighbor.print_conneted_points(all_labels_connections)
            neighbor.save_to_excel_json(
                all_labels_connections, output_folder, filename
            )

            neighbor.save_text_file(
                all_labels_connections,
                output_folder,
                filename,
                is_cn_used,
            )

            # Print progress
            elapsed_time = time.perf_counter() - start_time

            prompt.print_progress_finished(
                filename_with_ext,
                len(supercell_points),
                elapsed_time,
                is_finished=True,
            )
            all_labels_connections = None
