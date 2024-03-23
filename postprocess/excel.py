"""
Writes JSON and Excel files containing pair info
The following code will be refactored once results are confirmed.
"""

import os
import json
import pandas as pd


def write_site_pair_dict_to_excel_json(
    input_dict, pair_type, dir_path
):
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

    with pd.ExcelWriter(
        excel_file_path, engine="openpyxl"
    ) as excel_writer:
        for pair, files_info in input_dict.items():
            # Aggregate all info into a list of dictionaries to form a DataFrame
            aggregated_info = []
            for file_id, infos in files_info.items():
                for (
                    info
                ) in infos:  # Here infos is a list of dictionaries
                    info_copy = info.copy()
                    info_copy["File"] = (
                        f"{file_id}.cif"  # Add the file ID as 'File'
                    )
                    aggregated_info.append(info_copy)

            # Create a DataFrame from the aggregated information
            df = pd.DataFrame(aggregated_info)

            # Rename columns to match the expected format
            df.rename(
                columns={
                    "dist": "Distance",
                    "mixing": "Atomic Mixing",
                },
                inplace=True,
            )

            # Apply numeric transformation and category mapping
            df["Distance"] = pd.to_numeric(
                df["Distance"], errors="coerce"
            )
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
            df.to_excel(
                excel_writer, sheet_name=sheet_name, index=False
            )

    # Save JSON
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(input_dict, json_file, indent=4)

    print(f"Data has been saved to Excel and JSON in {output_dir}")


def write_element_pair_dict_to_excel_json(
    input_dict, pair_type, dir_path
):
    """
    Writes JSON and Excel files containing pair info,
    keeping only the shortest distance for each atomic mixing type.
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

    # Preprocess the input_dict to keep only the shortest distances for each atomic mixing
    for pair, files_info in input_dict.items():
        for file_id, infos in files_info.items():
            shortest_distances = {}
            for info in infos:
                mixing_type = info["mixing"]
                distance = float(info["dist"])
                if (
                    mixing_type not in shortest_distances
                    or distance
                    < float(shortest_distances[mixing_type]["dist"])
                ):
                    shortest_distances[mixing_type] = info
            input_dict[pair][file_id] = list(
                shortest_distances.values()
            )

    with pd.ExcelWriter(
        excel_file_path, engine="openpyxl"
    ) as excel_writer:
        for pair, files_info in input_dict.items():
            # Aggregate all info into a list of dictionaries to form a DataFrame
            aggregated_info = []
            for file_id, infos in files_info.items():
                for (
                    info
                ) in infos:  # Here infos is a list of dictionaries
                    info_copy = info.copy()
                    info_copy["File"] = (
                        f"{file_id}.cif"  # Add the file ID as 'File'
                    )
                    aggregated_info.append(info_copy)

            # Create a DataFrame from the aggregated information
            df = pd.DataFrame(aggregated_info)

            # Rename columns to match the expected format
            df.rename(
                columns={
                    "dist": "Distance",
                    "mixing": "Atomic Mixing",
                },
                inplace=True,
            )

            # Apply numeric transformation and category mapping
            df["Distance"] = pd.to_numeric(
                df["Distance"], errors="coerce"
            )
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
            df.to_excel(
                excel_writer, sheet_name=sheet_name, index=False
            )

    # Save JSON
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(input_dict, json_file, indent=4)

    print(f"Data has been saved to Excel and JSON in {output_dir}")
