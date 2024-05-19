import json
import pandas as pd
from preprocess import (
    cif_parser,
    cif_parser_handler,
    format,
)
from util import folder
from postprocess import neighbor


def main():
    dir_path = "20240518_shortest_dist_test"
    file_path_list = folder.get_cif_file_path_list(dir_path)
    # cutoff_radius = prompt.get_cutoff_radius()
    cutoff_radius = 3.9

    # PART 1: REFORMAT
    format.move_files_based_on_format_error(dir_path)
    folder.create_output_folder_for_neighbor(dir_path, cutoff_radius)

    # Dictionary to store connections for each label
    all_labels_connections = {}
    for i, file_path in enumerate(file_path_list):
        result = cif_parser_handler.get_cif_info(
            file_path, cif_parser.get_loop_tags()
        )
        _, lengths, angles, _, supercell_points, labels, _ = result

        unitcell_points = (
            cif_parser_handler.get_flattened_points_from_unitcell(
                file_path
            )
        )

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

    # Print all collected results
    print("All labels and their most connected points:")
    for label, connections in all_labels_connections.items():
        print(f"\nAtom site {label}:")
        for coord, dist in connections:
            print(f"{coord} {dist}")

    # Save the results to an Excel file
    with pd.ExcelWriter(
        "most_connected_points.xlsx", engine="openpyxl"
    ) as writer:
        for label, connections in all_labels_connections.items():
            # Convert the data into a DataFrame
            if (
                connections
            ):  # Check if there are any connections to save
                df = pd.DataFrame(
                    connections, columns=["Coordinate", "Distance"]
                )
                df.to_excel(writer, sheet_name=label, index=False)
                print(f"Data for {label} saved to Excel sheet.")
            else:
                print(
                    f"No data available for {label}, no sheet created."
                )


if __name__ == "__main__":
    main()
