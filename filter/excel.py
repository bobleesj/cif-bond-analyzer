import os
import shutil
import pandas as pd
import util.folder as folder
import textwrap

def choose_excel_file(script_directory):
    """"
    Lets the user choose an Excel file from the specified directory.
    """
    files = [f for f in os.listdir(script_directory) if f.endswith('.xlsx')]
    
    if not files:
        print("No Excel files found in the current path!")
        return None
    
    print("\nAvailable Excel files:")
    for idx, file_name in enumerate(files, start=1):
        print(f"{idx}. {file_name}")

    while True:
        try:
            choice = int(input("\nEnter the number corresponding to the Excel file: "))
            if 1 <= choice <= len(files):
                return os.path.join(script_directory, files[choice-1])
            else:
                print(f"Please enter a number between 1 and {len(files)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def choose_excel_sheet(excel_path):
    """
    Lets the user choose a sheet from the Excel file.
    """

    xls = pd.ExcelFile(excel_path)
    sheets = xls.sheet_names
    
    # Display available sheets
    print("\nAvailable sheets in the Excel file:")
    for idx, sheet_name in enumerate(sheets, start=1):
        print(f"{idx}. {sheet_name}")

    # User choice
    while True:
        try:
            choice = int(input("\nEnter the number corresponding to the Excel sheet: "))
            if 1 <= choice <= len(sheets):
                return sheets[choice-1]
            else:
                print(f"Please enter a number between 1 and {len(sheets)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def load_excel_data_to_set(excel_path, column_name, sheet_name):
    """Load data from a specific column of an Excel file into a set."""
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    # Convert all values to lowercase and strip whitespace, then add to set
    return set(df[column_name].values)


def extract_tag_from_line(line):
    """Extracts a tag from a line based on the format provided."""
    parts = [part.strip() for part in line.split("#") if part.strip()]  # Remove any empty parts
    if len(parts) >= 3:
        return parts[2]  # Return the CIF
    
    return None


def read_third_line(file_path):
    """Reads and returns the third line from a file."""
    with open(file_path, 'r') as file:
        for _ in range(2):
            file.readline()
        return extract_tag_from_line(file.readline())

def select_directory_and_file(script_directory):
    folder_info = folder.choose_CIF_directory(script_directory)
    if not folder_info:
        print("No folder selected.")
        return None, None

    excel_path = choose_excel_file(script_directory)
    if not excel_path:
        print("No Excel file selected.")
        return folder_info, None

    return folder_info, excel_path


def load_data_from_excel(excel_path):
    chosen_sheet_name = choose_excel_sheet(excel_path)
    column_name = "Entry"
    return load_excel_data_to_set(excel_path, column_name, chosen_sheet_name), chosen_sheet_name


def gather_cif_ids_from_files(folder_info):
    files_lst = [os.path.join(folder_info, file) for file in os.listdir(folder_info) if file.endswith('.cif')]
    
    cif_ids_in_files = set()
    for file_path in files_lst:
        CIF_id_string = read_third_line(file_path)
        try:
            CIF_id = int(CIF_id_string)
            cif_ids_in_files.add(CIF_id)
        except ValueError:
            print(f"Error: Invalid CIF ID in {os.path.basename(file_path)}")
            continue
    
    return cif_ids_in_files, len(files_lst)


def generate_and_save_report(folder_info, chosen_sheet_name, CIF_id_set_from_Excel, cif_ids_in_files, script_directory):
    """Generates and saves a report of missing CIF IDs compared to an Excel sheet."""
    folder_name = os.path.basename(folder_info)
    missing_cif_ids = CIF_id_set_from_Excel - cif_ids_in_files
    
   
    if missing_cif_ids:
        print("Missing CIF IDs:")
        for cif_id in missing_cif_ids:
            print(cif_id)
    else:
        print("Every CIF file in the chosen Excel sheet exists in the chosen folder")

    print("\nSummary:")
    print(f"- {len(missing_cif_ids)} entries from the Excel sheet are missing in the chosen CIF folder.\n")
        
    df_missing = pd.DataFrame(list(missing_cif_ids), columns=['Missing CIF IDs'])
    
    csv_filename = f"{folder_name}_missing_files.csv"
    csv_path = os.path.join(script_directory, csv_filename)
    
    df_missing.to_csv(csv_path, index=False)
    print(f"\nMissing CIF IDs saved to {csv_filename}.")

def filter_and_save_excel(excel_path, cif_ids_in_files, chosen_sheet_name):
    """
    Filters the original Excel sheet to only include the rows where the entry matches 
    the cif_ids_in_files and saves the modified DataFrame to a new Excel file.
    """
    df_original = pd.read_excel(excel_path, sheet_name=chosen_sheet_name)
    
    # Filter the dataframe
    df_filtered = df_original[df_original['Entry'].isin(cif_ids_in_files)]
    
    # Create the new filename
    base_name, ext = os.path.splitext(os.path.basename(excel_path))
    new_filename = base_name + '_filtered' + ext
    new_excel_path = os.path.join(os.path.dirname(excel_path), new_filename)
    
    # Save to the new Excel file
    df_filtered.to_excel(new_excel_path, index=False)
    print(f"\nFiltered Excel sheet saved to {new_filename}.")
    
    return new_excel_path


def get_new_Excel_with_matching_entries(script_directory):
    """Processes an Excel check by orchestrating multiple functions together."""
    introductory_paragraph = textwrap.dedent("""\
    ===
    Welcome to the CIF-Excel Matching Tool!

    You will be required to provide an Excel file that contains a list of CIF IDs.
    Next, select the CIF directory of your choice. This tool will then compare the entries in the 
    provided Excel sheet with the CIF files in the chosen directory. 

    Upon completion, two outputs will be generated:
    1. A new Excel file that will only have rows matching the CIF files present in the chosen directory.
    2. A CSV report showcasing the missing CIF IDs that are present in the Excel sheet but not found in the directory.

    Let's get started!
    ===
    """)
    
    print(introductory_paragraph)

    folder_info, excel_path = select_directory_and_file(script_directory)
    if not folder_info or not excel_path:
        print("Exiting.")
        return

    CIF_id_set_from_Excel, chosen_sheet_name = load_data_from_excel(excel_path)
    cif_ids_in_files, total_files = gather_cif_ids_from_files(folder_info)
    
    # Filter the original Excel and save to a new file
    filter_and_save_excel(excel_path, cif_ids_in_files, chosen_sheet_name)
    generate_and_save_report(folder_info, chosen_sheet_name, CIF_id_set_from_Excel, cif_ids_in_files, script_directory)

