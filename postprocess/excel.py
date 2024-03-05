import pandas as pd


def write_excel(unique_pair_tuple_list, global_pairs_data):
    # Initialize a dictionary to hold the pairs and the .cif files
    pairs_files_mapping = {}

    for pair in unique_pair_tuple_list:
        pairs_files_mapping[pair] = []
        for filename, pairs in global_pairs_data.items():
            # If the pair is present in the cif file
            if pair in pairs:
                pairs_files_mapping[pair].append(filename)

    # Sort pairs by the number of files they appear in, descending
    sorted_pairs = sorted(pairs_files_mapping.items(), key=lambda item: len(item[1]), reverse=True)

    # Print the mapping of pairs to files
    for pair, files in pairs_files_mapping.items():
        print(f"Pair {pair} is found in: {files}")

    # Create a Pandas Excel writer using openpyxl as the engine
    excel_writer = pd.ExcelWriter("unique_pairs.xlsx", engine='openpyxl')
    
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
        sheet_name = f"{pair[0]}-{pair[1]} ({len(files)})"
        df.to_excel(excel_writer, sheet_name=sheet_name[:31], index=False)


    # Save the Excel file
    excel_writer.close()