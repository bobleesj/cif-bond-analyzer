"""
Determines the nearest neighbor distances from each atomic site
based on the cutoff distance provided

Author: Sangjoon Bob Lee
Last update: May 18, 2024
Release date: Mar 10, 2024
"""

import os
import time
from click import style, echo
from preprocess import (
    cif_parser,
    cif_parser_handler,
    format,
)
from util import folder, prompt
from postprocess import neighbor


def main():
    dir_path = "20240518_shortest_dist_test"
    file_path_list = folder.get_cif_file_path_list(dir_path)
    cutoff_radius = prompt.get_cutoff_radius()

    # PART 1: REFORMAT
    format.move_files_based_on_format_error(dir_path)
    output_folder = folder.create_output_folder_for_neighbor(
        dir_path, cutoff_radius
    )

    # Dictionary to store connections for each label
    all_labels_connections = {}

    # PART 2: Process each file
    for i, file_path in enumerate(file_path_list):
        start_time = time.perf_counter()
        filename_with_ext = os.path.basename(file_path)
        filename, _ = os.path.splitext(filename_with_ext)
        result = cif_parser_handler.get_cif_info(
            file_path, cif_parser.get_loop_tags()
        )
        _, lengths, angles, _, supercell_points, labels, _ = result

        unitcell_points = (
            cif_parser_handler.get_flattened_points_from_unitcell(
                file_path
            )
        )

        echo(
            style(
                f"Processing {filename_with_ext} with "
                f"{len(supercell_points)} atoms {i+1}",
                fg="yellow",
            )
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
            label, connections = neighbor.get_most_connected_point(
                site_label, dist_dict, dist_set
            )

            all_labels_connections[label] = connections

        # Save Excel
        excel_file_path = os.path.join(
            output_folder, filename + ".xlsx"
        )
        neighbor.print_conneted_points(all_labels_connections)
        neighbor.save_to_excel(
            all_labels_connections, excel_file_path
        )

        # Print progress
        elapsed_time = time.perf_counter() - start_time

        prompt.print_progress(
            filename_with_ext,
            len(supercell_points),
            elapsed_time,
            is_finished=True,
        )


if __name__ == "__main__":
    main()
