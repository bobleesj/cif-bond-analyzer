import os
import json
import pandas as pd
from preprocess import cif_parser
from util import prompt


def clean_formula(formula):
    return formula.replace("~", "").replace(" ", "").replace("'", "")


def clean_structure_type(structure_type):
    return structure_type.split(",")[0].replace("~", "")


def write_json_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def read_json_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def update_json_data(data, cif_directory):
    unique_pairs = []
    unique_structure_types = []
    unique_formulas = []
    for key, site_pairs in data.items():
        print(f"Processing data for: {key}")
        unique_pairs.append(key)
        for cif_id, cif_data_list in site_pairs.items():
            cif_file_path = os.path.join(cif_directory, f"{cif_id}.cif")
            if os.path.exists(cif_file_path):
                try:
                    block = cif_parser.get_cif_block(cif_file_path)
                    formula = clean_formula(
                        block.find_value("_chemical_formula_structural")
                    )
                    structure_type = clean_structure_type(
                        block.find_value("_chemical_name_structure_type")
                    )
                    for pair in cif_data_list:
                        pair["formula"] = formula
                        pair["structure_type"] = structure_type
                    unique_structure_types.append(structure_type)
                    unique_formulas.append(formula)
                except Exception as e:
                    print(f"Failed to process {cif_file_path}: {e}")
            else:
                print(f"File not found: {cif_file_path}")
    return (
        data,
        unique_pairs,
        set(unique_structure_types),
        set(unique_formulas),
    )


def remove_structures_with_zero_counts(dict):
    structures_to_remove = []

    # Iterate over the items and check the file counts
    for formula, structures in dict.items():
        for structure_type, bonds in structures.items():
            if all(
                bond_info["file_count"] == 0 for bond_info in bonds.values()
            ):
                structures_to_remove.append(
                    (formula, structure_type)
                )  # Mark for removal

    # Remove the marked structure types
    for formula, structure_type in structures_to_remove:
        del dict[formula][structure_type]

    return dict


def add_bond_count_to_structure_dict(structure_dict, formula_dict):
    # Try to determine bond_count after remoivng duplicates
    # formula dict is used to get the file count
    for formula, pair_data in structure_dict.items():
        for structure, structure_data in pair_data.items():
            file_count = formula_dict[formula][structure]["file_count"]

            for bond_pair, bond_count_data in structure_data.items():
                bond_count = bond_count_data["bond_count"]
                structure_dict[formula][structure][bond_pair][
                    "file_count"
                ] = file_count
                if file_count > 1:
                    bond_count_no_duplicates = int(bond_count / file_count)
                    structure_dict[formula][structure][bond_pair][
                        "bond_count_no_duplicates"
                    ] = bond_count_no_duplicates
                else:
                    structure_dict[formula][structure][bond_pair][
                        "bond_count_no_duplicates"
                    ] = bond_count
    return structure_dict


def add_bond_dist_to_structure_dict(structure_dict, updated_site_pair_dict):
    prompt.print_dict_in_json(structure_dict)

    # Loop through each formula
    for formula, data in structure_dict.items():
        # Loop thruogh each structure
        for structure, data in data.items():
            # Loop through each bond
            for bond, data in data.items():
                # Find bond.\ then, match structure, then dist
                print(formula, structure, bond)

    # Add the average bond lenghts
    # Add the average STD
    prompt.print_dict_in_json(updated_site_pair_dict)
    return structure_dict


def initialize_structure_duplicate_dict(
    unique_formulas, unique_structure_types
):
    return {
        formula: {
            structure_type: {"file_count": 0}
            for structure_type in unique_structure_types
        }
        for formula in unique_formulas
    }


def initialize_system_analysis_dict(
    unique_formulas, unique_structure_types, bond_types
):
    return {
        formula: {
            structure_type: {
                bond: {
                    "bond_count": 0,
                    "bond_total_dist": 0.0,
                    "bond_avg_dist": 0.0,
                }
                for bond in bond_types
            }
            for structure_type in unique_structure_types
        }
        for formula in unique_formulas
    }


def add_no_duplicate_file_count(json_file_path, structure_dict, formula_dict):
    # Read the JSON file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Iterate through data to update dictionaries
    for bond_pair, pair_data in data.items():
        print(structure_dict)
        for _, cif_data in pair_data.items():
            is_file_counted = (
                False  # Tracker to ensure file is counted once per bond_pair
            )

            for data_item in cif_data:
                formula = data_item["formula"]
                structure_type = data_item["structure_type"]
                structure_dict[formula][structure_type][bond_pair][
                    "bond_count"
                ] += 1

                structure_dict[formula][structure_type][bond_pair][
                    "bond_total_dist"
                ] += float(data_item["dist"])

                if not is_file_counted:
                    formula_dict[formula][structure_type]["file_count"] += 1
                    is_file_counted = True

    # Use the total bond dist and the number of bonds to find the avg bond dist
    return structure_dict, formula_dict


def create_structure_sheet(system_analysis_dict):
    rows_list = []

    for formula, structures in system_analysis_dict.items():
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
                    "Unique bond count": bond_info.get(
                        "bond_count_no_duplicates", 0
                    ),
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
                    "Unique bond count": "",
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
        structure_df.groupby("Bond type")["Unique bond count"].sum().to_dict()
    )

    # Create dictionaries for the 'Total' row and 'Unique Total' row
    total_row = {"CIF #": "Total"}
    unique_total_row = {"CIF #": "No duplicates total"}
    for bond_pair in bond_pairs_list:
        bond_pair_string = f"{bond_pair[0]}-{bond_pair[1]}"
        total_row[bond_pair_string] = bond_count_totals.get(
            bond_pair_string, 0
        )
        unique_total_row[bond_pair_string] = unique_bond_count_totals.get(
            bond_pair_string, 0
        )

    # Convert the total_row and unique_total_row dictionaries to DataFrames
    total_df = pd.DataFrame([total_row], columns=df.columns)
    unique_total_df = pd.DataFrame([unique_total_row], columns=df.columns)

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
