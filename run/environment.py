import os
import time
from preprocess import (
    cif_parser,
    cif_parser_handler,
    format,
    supercell_handler,
)
from util import folder, prompt
from postprocess.environment import (
    env_util,
    environment_output,
    environment_neighbor,
    environment_cn,
)


def run_environment_analysis(script_path):
    """
    Determines the nearest neighbor distances from each atomic site
    based on the cutoff distance or coordination number.
    """

    is_cn_used = False
    cutoff_radius = 10
    # dir_name = "20240525_binary_test"
    dir_name = "20240525_ternary_env"
    dir_path = os.path.join(script_path, dir_name)
    file_path_list = folder.get_file_path_list(dir_path)

    # PART 1: Pre-process
    format.preprocess_move_files_based_on_format_error(dir_path)
    file_path_list = folder.get_file_path_list(dir_path)

    output_folder = folder.create_output_folder_for_neighbor(
        dir_path, cutoff_radius, is_cn_used
    )

    # PART 2: Process each file
    for i, file_path in enumerate(file_path_list):
        # Dictionary to store connections for each label
        start_time = time.perf_counter()
        filename_with_ext = os.path.basename(file_path)
        filename, _ = os.path.splitext(filename_with_ext)
        result = cif_parser_handler.get_cif_info(file_path)

        (
            _,
            formula,
            _,
            _,
        ) = cif_parser.get_phase_tag_formula_id_from_third_line(file_path)

        (
            _,
            lengths,
            angles,
            _,
            supercell_points,
            labels,
            _,
        ) = result

        unitcell_points = supercell_handler.get_flattened_points_from_unitcell(
            file_path
        )

        prompt.print_progress_current(
            i, filename_with_ext, supercell_points, len(file_path_list)
        )

        # PART 3: Process each atomic label
        all_labels_connections = (
            environment_neighbor.get_all_labels_connections(
                labels,
                unitcell_points,
                supercell_points,
                cutoff_radius,
                lengths,
                angles,
                is_cn_used,
            )
        )

        # neighbor.print_conneted_points(all_labels_connections)
        environment_output.save_to_excel_json(
            all_labels_connections, output_folder, filename
        )

        environment_output.save_text_file(
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

        distances_dict = env_util.get_pair_distances_dict_for_binary_ternary(
            all_labels_connections, formula
        )

        env_util.get_first_shortest_distances(distances_dict)
        env_util.get_second_sortest_distances(distances_dict)

        environment_cn.get_coordination_number_per_label()

    # dir_names_with_cif = folder.get_cif_dir_names(script_path)

    # # If no folders containing .cif files found, exit
    # if not dir_names_with_cif:
    #     return

    # cutoff_radius = None
    # is_cn_used = prompt.get_is_coordination_num_used()

    # if not is_cn_used:
    #     cutoff_radius = prompt.get_cutoff_radius()
    # else:
    #     # Default of 10. Later, connections will be filtered based on CN
    #     cutoff_radius = 10

    # selected_dirs = prompt.get_user_input_folder_processing(
    #     dir_names_with_cif, ".cif"
    # )

    # dir_names_with_cif = folder.get_cif_dir_names(script_path)

    # # If no folders containing .cif files found, exit
    # if not dir_names_with_cif:
    #     return

    # is_cn_used = True
    # cutoff_radius = 10
    # num_selected_dirs = len(selected_dirs)

    # for idx, dir_name in enumerate(selected_dirs.values(), start=1):
    #     dir_path = os.path.join(script_path, dir_name)
    #     file_path_list = folder.get_file_path_list(dir_path)
    #     prompt.echo_folder_progress(idx, dir_name, num_selected_dirs)

    #     # PART 1: Pre-process
    #     format.move_files_based_on_format_error(dir_path)
    #     file_path_list = folder.get_file_path_list(dir_path)

    #     output_folder = folder.create_output_folder_for_neighbor(
    #         dir_path, cutoff_radius, is_cn_used
    #     )

    #     # PART 2: Process each file
    #     for i, file_path in enumerate(file_path_list):
    #         # Dictionary to store connections for each label
    #         start_time = time.perf_counter()
    #         filename_with_ext = os.path.basename(file_path)
    #         filename, _ = os.path.splitext(filename_with_ext)
    #         result = cif_parser_handler.get_cif_info(file_path)
    #         (
    #             _,
    #             lengths,
    #             angles,
    #             _,
    #             supercell_points,
    #             labels,
    #             _,
    #         ) = result

    #         unitcell_points = (
    #             supercell_handler.get_flattened_points_from_unitcell(file_path)
    #         )

    #         prompt.print_progress_current(
    #             i, filename_with_ext, supercell_points, len(file_path_list)
    #         )

    #         # PART 3: Process each atomic label
    #         all_labels_connections = (
    #             environment_neighbor.get_all_labels_connections(
    #                 labels,
    #                 unitcell_points,
    #                 supercell_points,
    #                 cutoff_radius,
    #                 lengths,
    #                 angles,
    #                 is_cn_used,
    #             )
    #         )

    #         # neighbor.print_conneted_points(all_labels_connections)
    #         environment_output.save_to_excel_json(
    #             all_labels_connections, output_folder, filename
    #         )

    #         environment_output.save_text_file(
    #             all_labels_connections,
    #             output_folder,
    #             filename,
    #             is_cn_used,
    #         )

    #         # Print progress
    #         elapsed_time = time.perf_counter() - start_time

    #         prompt.print_progress_finished(
    #             filename_with_ext,
    #             len(supercell_points),
    #             elapsed_time,
    #             is_finished=True,
    #         )

    #         environment_util.get_pair_shortest_dists_for_binary_teranry(
    #             all_labels_connections, True
    #         )
