import shutil
import pandas as pd
import os
import util.folder as folder
import filter.tags as tags


def extract_formula_and_tag(compound_formula_tag):
    parts = compound_formula_tag.split()
    
    # First part is the compound formula
    compound_formula = parts[0]
    
    # The rest are tags
    tags = "_".join(parts[1:])
    
    return compound_formula, tags

def move_files_based_on_tags(script_directory, is_interactive_mode=True):
    print("This script sorts CIF files based on specific tags present in their third line.")
    
    print("Script directory",script_directory)
    folder_info = ""

    # With graphic user interface
    if is_interactive_mode:
        print(folder_info)
        folder_info = folder.choose_CIF_directory(script_directory)
        folder_name = os.path.basename(folder_info)
    
    # No graphic user interface - enter the folder path
    if not is_interactive_mode:
        print(folder_info)
        folder_info = script_directory
        folder_name = os.path.basename(folder_info)

    # Create an empty dataframe to track the moved files
    df = pd.DataFrame(columns=['Filename', 'Formula', 'Tag(s)'])

    # Get a list of all .cif files in the chosen directory
    files_lst = [os.path.join(folder_info, file) for file in os.listdir(folder_info) if file.endswith('.cif')]
    total_files = len(files_lst)

    # Iterate through each .cif file, extract its tag and sort it accordingly
    for idx, file_path in enumerate(files_lst, start=1):
        folder_name = os.path.basename(folder_info)
        filename = os.path.basename(file_path)
        print(f"Processing {filename}, ({idx}/{total_files})")

        # Extracts the compound name and tag from the provided CIF file path.
        with open(file_path, 'r') as f:
            f.readline()  # First line
            f.readline()  # Second line
            third_line = f.readline().strip()  # Third line
            third_line = third_line.replace(",", "")

            third_line_parts = [part.strip() for part in third_line.split("#") if part.strip()]

            compound_formula, tags = extract_formula_and_tag(third_line_parts[1])
            print("Formula:", compound_formula, "Tags:", tags)

            if tags:
                subfolder_path = os.path.join(folder_info, f"{folder_name}_{tags}")
                new_file_path = os.path.join(subfolder_path, filename)
                new_row_df = pd.DataFrame({'Filename': [filename], 'Formula': [compound_formula], 'Tag(s)': [tags]})
                df = pd.concat([df, new_row_df], ignore_index=True)

                if not os.path.exists(subfolder_path):
                    os.makedirs(subfolder_path)

                # Delete if file already exists at destination
                if os.path.exists(new_file_path):
                    os.remove(new_file_path)

                shutil.move(file_path, subfolder_path)
                print(f"{os.path.basename(file_path)} has been moved to {subfolder_path}")

            print()

    folder.save_to_csv_directory(folder_info, df, "tags_log")
