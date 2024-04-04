import os
import json
import click
from click import echo
import numpy as np
from preprocess import cif_parser, cif_parser_handler, supercell, format
from util import prompt, folder


def get_cutoff_dist_info():
    """
    Main function to process CIF files, calculate distances between atom sites,
    and save the information in JSON files.
    """
    main_script_path = os.path.dirname(os.path.abspath(__file__))
    dir_names_with_cif = folder.get_cif_dir_names(main_script_path)
    selected_dirs = prompt.get_user_input_folder_processing(
        dir_names_with_cif, ".cif"
    )
    cutoff_radius = click.prompt(
        "\nEnter the cut-off distance from the reference atom site (Å) (Default 3 Å)",
        type=float,
        default=3,
        show_default=False,
    )

    # Get the number of chosen cif folders
    num_selected_dirs = len(selected_dirs)

    # Process each folder
    for idx, dir_name in enumerate(selected_dirs.values(), start=1):
        prompt.echo_folder_progress(idx, dir_name, num_selected_dirs)
        dir_path = os.path.join(main_script_path, dir_name)
        # PART 1: REFORMAT
        format.move_files_based_on_format_error(dir_path)
        output_folder_path = os.path.join(dir_path, "output")

        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        # Define and create the nested folder based on the cutoff radius
        nested_folder_name = f"shortest_dist_cutoff_{cutoff_radius}"
        nested_folder_path = os.path.join(
            output_folder_path, nested_folder_name
        )

        if not os.path.exists(nested_folder_path):
            os.makedirs(nested_folder_path)

        file_path_list = folder.get_cif_file_path_list(dir_path)

        # Process each file in the folder
        for i, file_path in enumerate(file_path_list, start=1):
            result = cif_parser_handler.get_cif_info(
                file_path, cif_parser.get_loop_tags()
            )
            _, lengths, angles_rad, _, all_points, unique_labels, _ = result

            # Initialize the dictionary to hold cutoff distance information
            cutoff_dist_info = {}

            # Process each atomic site in the file
            for label in unique_labels:
                point1 = next(
                    (point for point in all_points if point[3] == label), None
                )
                if not point1:
                    continue

                fractional_coord_1 = [point1[0], point1[1], point1[2]]
                cart_coords_point_1 = supercell.fractional_to_cartesian(
                    fractional_coord_1, lengths, angles_rad
                )

                cutoff_dist_info[label] = {
                    "coord": np.round(cart_coords_point_1, 3).tolist(),
                    "connections": [],
                }

                for point2 in all_points:
                    if point1[:3] == point2[:3]:
                        continue

                    frac_coord_2 = [point2[0], point2[1], point2[2]]
                    cart_coords_point_2 = supercell.fractional_to_cartesian(
                        frac_coord_2, lengths, angles_rad
                    )

                    dist = supercell.calc_dist_two_cart_points(
                        cart_coords_point_1, cart_coords_point_2
                    )
                    if dist <= cutoff_radius:
                        cutoff_dist_info[label]["connections"].append(
                            {
                                "label": point2[3],
                                "coord": np.round(
                                    cart_coords_point_2, 3
                                ).tolist(),
                                "distance": np.round(dist, 3),
                            }
                        )

            filename_with_extension = os.path.basename(file_path)
            filename, _ = os.path.splitext(filename_with_extension)

            # Save JSON
            output_file_path = os.path.join(
                nested_folder_path, f"{filename}.json"
            )
            with open(output_file_path, "w") as outfile:
                json.dump(cutoff_dist_info, outfile, indent=4)
            echo(
                f"Processed {filename_with_extension}, ({i} out of {len(file_path_list)})"
            )
        print("JSONs saved to", nested_folder_path)


if __name__ == "__main__":
    get_cutoff_dist_info()
