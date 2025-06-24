"""Writes JSON and Excel files containing pair info The following code
will be refactored once results are confirmed."""

import json
import os

import pandas as pd
from cifkit.utils.folder import make_output_folder


def save_excel_json(
    global_site_pair_dict,
    global_element_pair_dict,
    dir_path,
):
    # Create folder
    output_dir_path = make_output_folder(dir_path, "output")
    # Save Excel file (1/2) with site pair
    write_pair_dict_to_excel_json(
        global_site_pair_dict, "site", dir_path, output_dir_path
    )

    # Save Excel file (2/2) with shortest element pair
    write_pair_dict_to_excel_json(
        global_element_pair_dict, "element", dir_path, output_dir_path
    )


def write_pair_dict_to_excel_json(
    input_dict, pair_type, dir_path, output_dir_path
):
    """Writes JSON and Excel files containing pair info, adjusted.

    Computes and saves the average and standard deviation for the
    distance.
    """

    folder_name = os.path.basename(os.path.normpath(dir_path))
    excel_file_path = os.path.join(
        output_dir_path, f"{folder_name}_{pair_type}_pairs.xlsx"
    )
    json_file_path = os.path.join(
        output_dir_path, f"{folder_name}_{pair_type}_pairs.json"
    )

    with pd.ExcelWriter(excel_file_path, engine="openpyxl") as excel_writer:
        for pair, files_info in input_dict.items():
            aggregated_info = []
            for file_id, infos in files_info.items():
                for info in infos:  # Here infos is a list of dictionaries
                    info_copy = info.copy()
                    info_copy["File"] = f"{file_id}.cif"
                    aggregated_info.append(info_copy)

            df = pd.DataFrame(aggregated_info)
            df.rename(
                columns={
                    "dist": "Distance",
                    "mixing": "Atomic Mixing",
                },
                inplace=True,
            )

            df["Distance"] = pd.to_numeric(df["Distance"], errors="coerce")
            df["Atomic Mixing"] = (
                df["Atomic Mixing"].astype(str).fillna("Unknown")
            )
            df.sort_values(by="Distance", inplace=True)
            df = df[["File", "Distance", "Atomic Mixing"]]

            # Calculate average and standard deviation for Distance
            average = round(df["Distance"].mean(), 3)
            std_dev = round(df["Distance"].std(), 3)

            # Create a blank row and summary rows
            blank_row = {
                "File": None,
                "Distance": None,
                "Atomic Mixing": None,
            }
            summary_rows = [
                blank_row,
                {
                    "File": "Average",
                    "Distance": average,
                    "Atomic Mixing": None,
                },
                {
                    "File": "SD",
                    "Distance": std_dev,
                    "Atomic Mixing": None,
                },
            ]

            # Append the summary rows to the DataFrame
            summary_df = pd.DataFrame(summary_rows)
            final_df = pd.concat([df, summary_df], ignore_index=True)

            sheet_name = pair[:31]  # Excel sheet name limit
            final_df.to_excel(
                excel_writer,
                sheet_name=sheet_name,
                index=False,
            )
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(input_dict, json_file, indent=4)
