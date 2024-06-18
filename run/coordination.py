from util import folder, prompt
import pandas as pd
from cifkit import Cif, CifEnsemble
from cifkit.utils import string_parser
import numpy as np


def run_coordination(script_path):
    dir_names_with_cif = folder.get_cif_dir_names(
        script_path
    )
    selected_dirs = prompt.get_user_input_folder_processing(
        dir_names_with_cif, ".cif"
    )
    process_each_folder(selected_dirs)
    


def process_each_folder(selected_dirs):
    num_selected_dirs = len(selected_dirs)
    for idx, dir_name in enumerate(
        selected_dirs.values(), start=1
    ):
        output_dir = folder.create_folder_under_output_dir(dir_name, "coordination")
        prompt.echo_folder_progress(
            idx, dir_name, num_selected_dirs
            
        )
        # Initialize the CIF ensemble
        cif_ensemble = CifEnsemble(dir_name)
        file_paths = cif_ensemble.file_paths
        
        # Get radius data
        df = pd.read_excel("radii.xlsx", sheet_name="data")

        # Create an Excel writer object
        writer = pd.ExcelWriter(
            f"{output_dir}/{dir_name}_CN_connections.xlsx", engine="openpyxl"
        )

        # Process each file
        for file_path in file_paths:
            cif = Cif(file_path)
            connection_data = (
                cif.CN_connections_by_best_methods
            )

            # Create a list to store
            all_data_for_excel = []

            # Iterate over connection data and collect information
            for (
                label,
                connections,
            ) in connection_data.items():
                ref_element = (
                    string_parser.get_atom_type_from_label(
                        label
                    )
                )
                ref_element_rad = df.loc[
                    df["Element"] == ref_element, "Radius"
                ].values[0]

                is_ref_element_text_written = False

                for connection in connections:
                    # Append a row for each connection
                    other_label = connection[0]
                    dist = connection[1]

                    other_element = string_parser.get_atom_type_from_label(
                        other_label
                    )
                    other_element_rad = df.loc[
                        df["Element"] == other_element,
                        "Radius",
                    ].values[0]

                    rad_sum = (
                        ref_element_rad + other_element_rad
                    )
                    if not is_ref_element_text_written:
                        all_data_for_excel.append(
                            {
                                "Reference_label": label,
                                "Other_label": other_label,
                                "Distance_Å": dist,
                                "∆ (%)": np.round(
                                    (float(dist) - rad_sum)
                                    * 100
                                    / rad_sum,
                                    3,
                                ),
                            }
                        )
                    else:
                        all_data_for_excel.append(
                            {
                                "Reference_label": "",
                                "Other_label": other_label,
                                "Distance_Å": dist,
                                "∆ (%)": np.round(
                                    (float(dist) - rad_sum)
                                    * 100
                                    / rad_sum,
                                    3,
                                ),
                            }
                        )
                    is_ref_element_text_written = True

                # Add an empty row after each label's connections
                all_data_for_excel.append({})

            # Convert the list of dictionaries to a DataFrame
            df_temp = pd.DataFrame(all_data_for_excel)

            # Get the formula from the CIF and use it as sheet name
            sheet_name = cif.formula

            # Save the DataFrame to a separate sheet in the Excel file
            df_temp.to_excel(
                writer, sheet_name=sheet_name, index=False
            )

        # Save the Excel file
        writer._save()
        print(
            f"Data successfully written {output_dir}.xlsx"
        )
