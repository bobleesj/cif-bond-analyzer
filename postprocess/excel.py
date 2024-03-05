import pandas as pd
import os
import json


def write_excel(dir_path, unique_pair_tuple_list, global_pairs_data):
    # Initialize a dictionary to hold the pairs and the .cif files
    pairs_files_mapping = {}
    json_data = {}

    for pair in unique_pair_tuple_list:
        pairs_files_mapping[pair] = []
        for filename, pairs in global_pairs_data.items():
            # If the pair is present in the cif file
            if pair in pairs:
                pairs_files_mapping[pair].append(filename)

    # Sort pairs by the number of files they appear in, descending
    sorted_pairs = sorted(
        pairs_files_mapping.items(),
        key=lambda item: len(item[1]),
        reverse=True
    )

    # Print the mapping of pairs to files
    for pair, files in pairs_files_mapping.items():
        print(f"Pair {pair} is found in: {files}")

    # Prepare the output directory
    output_dir = os.path.join(dir_path, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prepare the Excel file path
    folder_name = os.path.basename(os.path.normpath(dir_path))
    excel_file_path = os.path.join(output_dir, f"{folder_name}_pairs.xlsx")

    # Create a Pandas Excel writer using openpyxl as the engine
    excel_writer = pd.ExcelWriter(excel_file_path, engine='openpyxl')

    # Iterate over each unique pair
    for pair, files in sorted_pairs:
        # Initialize a list to hold the data for this pair
        data_for_pair = []

        # For each file that contains this pair, add the filename and dist
        for file in files:
            distance = float(global_pairs_data[file][pair])
            data_for_pair.append({'File': file, 'Distance': distance})

        # Sort the data for the pair by distance, from shortest to longest
        sorted_data_for_pair = sorted(data_for_pair, key=lambda x: x['Distance'])

        # Convert the sorted list to a DataFrame
        df = pd.DataFrame(sorted_data_for_pair)

        # Prepare sheet name including the count
        sheet_name = f"{pair[0]}-{pair[1]}"

        # Older Excel supports up to 31 sheets only.
        df.to_excel(excel_writer, sheet_name=sheet_name[:31], index=False)

        # Convert the DataFrame to JSON and save
        json_data[f"{pair[0]}-{pair[1]}"] = sorted_data_for_pair

    # Save the Excel file
    excel_writer.close()

    # Prepare the JSON file path
    json_file_path = os.path.join(output_dir, f"{folder_name}_pairs.json")

    # Write the JSON data to a single file
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
