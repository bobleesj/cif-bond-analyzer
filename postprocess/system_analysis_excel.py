import pandas as pd


def create_structure_sheet(structure_dict):
    rows_list = []

    for formula, structures in structure_dict.items():
        for structure_type, bonds in structures.items():
            # Temporary list to hold a chunk of rows
            temp_structure_rows = []

            for bond_type, bond_info in bonds.items():
                bond_count = bond_info.get("bond_count", 0)

                # Create a row for each bond type only if bond count is non-zero
                row = {
                    "Formula": formula,
                    "Structure": structure_type,
                    "Bond type": bond_type,
                    "Bond count": bond_count,
                    "No duplicate bond count": bond_info.get(
                        "bond_count_no_duplicates", 0
                    ),
                    "Average bond length": bond_info.get("bond_avg_dist", 0),
                    "Std dev": bond_info.get("bond_std_dev", 0),
                }
                temp_structure_rows.append(row)

            # Extend the main list with the temporary list of rows
            rows_list.extend(temp_structure_rows)
            # Append a blank row for separation
            rows_list.append(
                {
                    "Formula": "",
                    "Structure": "",
                    "Bond type": "",
                    "Bond count": "",
                    "No duplicate bond count": "",
                    "Average bond length": "",
                    "Std dev": "",
                }
            )

    # Create DataFrame from the list of dictionaries
    df = pd.DataFrame(rows_list)
    return df


def create_overview_sheet(
    json_data,
    bond_pairs_list,
    structure_df,
    excel_file_name="system_analysis_overview.xlsx",
):
    # Define the column order based on bond_pairs_list
    columns = ["CIF #"] + [f"{pair[0]}-{pair[1]}" for pair in bond_pairs_list]

    # Initialize an empty list to hold all CIF entries
    cif_entries = []

    # Create a set of all CIF IDs across all bond types
    cif_ids = {
        cif_id for bond_type in json_data for cif_id in json_data[bond_type]
    }

    # Iterate over each CIF ID
    for cif_id in cif_ids:
        entry = {"CIF #": cif_id}
        # For each bond pair, check if it is in the data and count the entries
        for bond_pair in bond_pairs_list:
            bond_pair_string = f"{bond_pair[0]}-{bond_pair[1]}"
            bond_data = json_data.get(bond_pair_string, {})
            entry[bond_pair_string] = len(bond_data.get(cif_id, []))
        # Add the entry to the list
        cif_entries.append(entry)

    # Create a DataFrame from the list of entries with the specified column order
    df = pd.DataFrame(cif_entries, columns=columns)

    # Extract the totals from the structure_df
    bond_count_totals = (
        structure_df.groupby("Bond type")["Bond count"].sum().to_dict()
    )
    unique_bond_count_totals = (
        structure_df.groupby("Bond type")["No duplicate bond count"]
        .sum()
        .to_dict()
    )

    # Create dictionaries for the 'Total' row and 'Unique Total' row
    total_count_row = {"CIF #": "Total"}
    no_duplicate_count_row = {"CIF #": "No duplicates total"}
    for bond_pair in bond_pairs_list:
        bond_pair_string = f"{bond_pair[0]}-{bond_pair[1]}"
        total_count_row[bond_pair_string] = bond_count_totals.get(
            bond_pair_string, 0
        )
        no_duplicate_count_row[
            bond_pair_string
        ] = unique_bond_count_totals.get(bond_pair_string, 0)

    # Convert the total_row and unique_total_row dictionaries to DataFrames
    total_df = pd.DataFrame([total_count_row], columns=df.columns)
    unique_total_df = pd.DataFrame(
        [no_duplicate_count_row], columns=df.columns
    )

    # Append the totals and unique totals DataFrames to the original DataFrame
    df = pd.concat([df, total_df, unique_total_df], ignore_index=True)

    # Calculate the fraction based on the "Total" row
    total_bonds = df.loc[df["CIF #"] == "Total", df.columns[1:]].iloc[0]
    fraction_row = (
        total_bonds / total_bonds.sum() if total_bonds.sum() != 0 else 0
    )
    fraction_df = pd.DataFrame([fraction_row], columns=df.columns[1:])
    fraction_df["CIF #"] = "Fraction"

    # Append the fraction DataFrame to the original DataFrame
    df = pd.concat([df, fraction_df], ignore_index=True)

    # Export the DataFrame to an Excel file
    df.to_excel(
        excel_file_name,
        index=False,
        sheet_name="system overview",
    )

    return df
