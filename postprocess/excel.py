"""
Writes JSON and Excel files containing pair info
The following code will be refactored once results are confirmed.
"""

import os
import json
import pandas as pd


def write_label_pair_dict_to_excel_json(input_dict, pair_tpye, dir_path):
    """
    Writes JSON and Excel files containing pair info.
    """
    output_dir = os.path.join(dir_path, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    folder_name = os.path.basename(os.path.normpath(dir_path))
    excel_file_path = os.path.join(
        output_dir, f"{folder_name}_{pair_tpye}_pairs.xlsx"
    )
    json_file_path = os.path.join(
        output_dir, f"{folder_name}_{pair_tpye}_pairs.json"
    )

    category_mapping = {
        1: "deficiency",
        2: "full_occupancy_atomic_mixing",
        3: "deficiency_no_atomic_mixing",
        4: "full_occupancy",
    }

    with pd.ExcelWriter(excel_file_path, engine="openpyxl") as excel_writer:
        for pair, files_info in input_dict.items():
            # Convert files_info dict to a DataFrame directly
            df = pd.DataFrame.from_dict(files_info, orient="index")
            df.reset_index(inplace=True)
            df.rename(
                columns={
                    "index": "File",
                    "dist": "Distance",
                    "mixing": "Atomic Mixing",
                },
                inplace=True,
            )

            df["Distance"] = pd.to_numeric(
                df["Distance"], errors="coerce"
            ).astype(float)

            # Convert 'Atomic Mixing' column to numeric, coerce errors
            df["Atomic Mixing"] = df["Atomic Mixing"].apply(
                pd.to_numeric, errors="coerce"
            )
            df["Atomic Mixing"] = (
                df["Atomic Mixing"].map(category_mapping).fillna("Unknown")
            )
            df["File"] = df["File"].apply(lambda x: f"{x}.cif")
            df.sort_values(by="Distance", inplace=True)

            # Specify the desired column order
            df = df[["File", "Distance", "Atomic Mixing"]]

            # Write DataFrame to Excel
            sheet_name = f"{pair[:31]}"  # Excel sheet name limit
            df.to_excel(excel_writer, sheet_name=sheet_name, index=False)

    # Save JSON
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(input_dict, json_file, indent=4)

    print(f"Data has been saved to Excel and JSON in {output_dir}")


def write_element_pair_dict_to_excel_json(input_dict, pair_type, dir_path):
    """
    Writes JSON and Excel files containing pair info, adjusted.
    """
    output_dir = os.path.join(dir_path, "output")
    os.makedirs(output_dir, exist_ok=True)

    folder_name = os.path.basename(os.path.normpath(dir_path))
    excel_file_path = os.path.join(
        output_dir, f"{folder_name}_{pair_type}_pairs.xlsx"
    )
    json_file_path = os.path.join(
        output_dir, f"{folder_name}_{pair_type}_pairs.json"
    )

    category_mapping = {
        "1": "deficiency",
        "2": "full_occupancy_atomic_mixing",
        "3": "deficiency_no_atomic_mixing",
        "4": "full_occupancy",
    }

    with pd.ExcelWriter(excel_file_path, engine="openpyxl") as excel_writer:
        for pair, files_info in input_dict.items():
            # Aggregate all info into a list of dictionaries to form a DataFrame
            aggregated_info = []
            for file_id, infos in files_info.items():
                for info in infos:  # Here infos is a list of dictionaries
                    info_copy = info.copy()
                    info_copy[
                        "File"
                    ] = f"{file_id}.cif"  # Add the file ID as 'File'
                    aggregated_info.append(info_copy)

            # Create a DataFrame from the aggregated information
            df = pd.DataFrame(aggregated_info)

            # Rename columns to match the expected format
            df.rename(
                columns={"dist": "Distance", "mixing": "Atomic Mixing"},
                inplace=True,
            )

            # Apply numeric transformation and category mapping
            df["Distance"] = pd.to_numeric(df["Distance"], errors="coerce")
            df["Atomic Mixing"] = (
                df["Atomic Mixing"]
                .astype(str)
                .map(category_mapping)
                .fillna("Unknown")
            )
            df.sort_values(by="Distance", inplace=True)

            # Specify the desired column order
            df = df[["File", "Distance", "Atomic Mixing"]]

            # Write DataFrame to Excel
            sheet_name = pair[:31]  # Excel sheet name limit
            df.to_excel(excel_writer, sheet_name=sheet_name, index=False)

    # Save JSON
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(input_dict, json_file, indent=4)

    print(f"Data has been saved to Excel and JSON in {output_dir}")
