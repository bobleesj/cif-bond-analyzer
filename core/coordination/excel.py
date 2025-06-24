import time
import pandas as pd
from cifkit import CifEnsemble
from core.prompts.progress import (
    prompt_progress_current,
    prompt_progress_finished,
)
from core.coordination.util import compute_delta
from core.prompts.progress import prompt_file_saved


def save_excel_for_connections(cif_ensemble: CifEnsemble, output_dir: str) -> None:
    """
    Save the coordination number connections for a set of CIF files
    in Excel format.
    """
    # Create an Excel writer object
    file_path = f"{output_dir}/CN_connections.xlsx"
    writer = pd.ExcelWriter(
        file_path,
        engine="openpyxl",
    )
    file_count = cif_ensemble.file_count
    # Process each file
    for i, cif in enumerate(cif_ensemble.cifs, start=1):
        start_time = time.perf_counter()
        prompt_progress_current(i, cif.file_name, cif.supercell_atom_count, file_count)
        # Lazy loading - this is the computaitonally intensive step
        cif.compute_CN()
        connection_data = cif.CN_connections_by_best_methods
        # Create a list to store
        all_data_for_excel = []

        # Iterate over connection data and collect information
        for label, connections in connection_data.items():
            # Used to add an empty row after a label
            is_ref_element_text_written = False

            for connection in connections:
                # Append a row for each connection
                other_label = connection[0]
                dist = connection[1]
                delta_percent = compute_delta(label, other_label, dist)

                if not is_ref_element_text_written:
                    data_row = {
                        "Reference_label": label,
                        "Other_label": other_label,
                        "Distance_Å": dist,
                        "∆ (%)": delta_percent,
                    }
                    all_data_for_excel.append(data_row)

                else:
                    data_row = {
                        "Reference_label": "",
                        "Other_label": other_label,
                        "Distance_Å": dist,
                        "∆ (%)": delta_percent,
                    }
                    all_data_for_excel.append(data_row)

                is_ref_element_text_written = True

            # Add an empty row after each label's connections
            all_data_for_excel.append({})

        # Convert the list of dictionaries to a DataFrame
        df_temp = pd.DataFrame(all_data_for_excel)

        # Get the formula from the CIF and use it as sheet name
        file_name_without_ext = cif.file_name_without_ext or "UnnamedFile"
        formula = cif.formula or "UnknownFormula"
        sheet_name = f"{file_name_without_ext}_{formula}"

        # Time
        elapsed_time = time.perf_counter() - start_time
        df_temp.to_excel(writer, sheet_name=sheet_name, index=False)
        prompt_progress_finished(cif.file_name, cif.supercell_atom_count, elapsed_time)

    # Save the Excel file
    writer._save()
    prompt_file_saved(file_path)
