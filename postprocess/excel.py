import os
import json
import pandas as pd


def write_excel_json(dist_mix_pair_dict, dir_path):
    output_dir = os.path.join(dir_path, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    folder_name = os.path.basename(os.path.normpath(dir_path))
    excel_file_path = os.path.join(output_dir, f"{folder_name}_pairs.xlsx")
    json_file_path = os.path.join(output_dir, f"{folder_name}_pairs.json")

    category_mapping = {
        1: "deficiency",
        2: "full_occupancy_atomic_mixing",
        3: "deficiency_no_atomic_mixing",
        4: "full_occupancy"
    }
    
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as excel_writer:
        for pair, files_info in dist_mix_pair_dict.items():
            # Convert files_info dict to a DataFrame directly
            df = pd.DataFrame.from_dict(files_info, orient='index')
            df.reset_index(inplace=True)
            df.rename(columns={
                'index': 'File',
                'dist': 'Distance',
                'mixing': 'Atomic Mixing'
            }, inplace=True)
            
            df['Distance'] = pd.to_numeric(
                df['Distance'], errors='coerce').astype(float)
             
            df['Atomic Mixing'] = df['Atomic Mixing'].apply(pd.to_numeric, errors='coerce').map(category_mapping).fillna("Unknown category")
            df['File'] = df['File'].apply(lambda x: f"{x}.cif")
            df.sort_values(by='Distance', inplace=True)
            
            # Specify the desired column order
            df = df[['File', 'Distance', 'Atomic Mixing']]

            # Write DataFrame to Excel
            sheet_name = f"{pair[:31]}"  # Excel sheet name limit
            df.to_excel(excel_writer, sheet_name=sheet_name, index=False)

    # Save JSON
    with open(json_file_path, 'w') as json_file:
        json.dump(dist_mix_pair_dict, json_file, indent=4)

    print(f"Data has been saved to Excel and JSON in {output_dir}")
