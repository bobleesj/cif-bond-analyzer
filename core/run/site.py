import os
import time
import pandas as pd
from click import echo

from core.site import (
    bond_missing,
    excel,
    histogram,
    writer,
)
from core.util import folder, prompt
from core.site import handler as site_handler
from cifkit import CifEnsemble, Cif
from core.util.save import save_to_json


def run_site_analysis(
    script_path,
):
    """Runs the bond extraction procedure"""
    prompt.prompt_site_analysis_intro()
    dir_names_with_cif = folder.get_cif_dir_names(script_path)
    selected_dirs = prompt.get_user_input_folder_processing(
        dir_names_with_cif, ".cif"
    )

    num_selected_dirs = len(selected_dirs)
    for idx, dir_path in enumerate(selected_dirs.values(), start=1):
        overall_start_time = time.perf_counter()
        prompt.echo_folder_progress(idx, dir_path, num_selected_dirs)
        cif_ensemble = CifEnsemble(dir_path)
        site_data = site_handler.get_site_pair_data_ordered_by_mendeleev(
            cif_ensemble
        )

        save_to_json(site_data, "site_site_pair_data.json")
        site_unique_element_pair_data = (
            site_handler.filter_with_minimum_distance_per_file(site_data)
        )
        save_to_json(
            site_unique_element_pair_data, "site_element_pair_data.json"
        )


# save_outputs(
#     global_site_pair_dict,
#     global_element_pair_dict,
#     dir_name,
#     file_path_list,
#     log_list,
#     overall_start_time,
# )

# def save_outputs(
#     global_site_pair_dict,
#     global_element_pair_dict,
#     dir_path,
#     file_path_list,
#     log_list,
#     overall_start_time,
# ):
#     missing_element_pairs = bond_missing.get_sorted_missing_pairs(
#         global_element_pair_dict
#     )

#     # PART 4: SAVE & PLOT
#     if len(file_path_list) > 0:
#         # Create a directory if needed
#         output_directory_path = os.path.join(dir_path, "output")

#         # Check if the output directory exists, create it if it does not
#         if not os.path.exists(output_directory_path):
#             os.makedirs(output_directory_path)

#         excel.save_excel_json(
#             global_site_pair_dict,
#             global_element_pair_dict,
#             dir_path,
#         )

#         # Save text file with element pairs
#         writer.write_summary_and_missing_pairs_with_element_dict(
#             global_element_pair_dict,
#             missing_element_pairs,
#             "summary_element.txt",
#             dir_path,
#         )

#         echo("Generating histograms...")
#         # Draw histograms
#         histogram.draw_histograms(
#             global_site_pair_dict,
#             global_element_pair_dict,
#             dir_path,
#         )

#         echo("Histograms saved.")

#         # Save log csv
#         folder.save_to_csv_directory(dir_path, pd.DataFrame(log_list), "log")
#         total_elapsed_time = time.perf_counter() - overall_start_time
#         echo(f"Total processing time: {total_elapsed_time:.2f}s")
