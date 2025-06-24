from os.path import join

import numpy as np
import pandas as pd

from core.prompts.progress import prompt_file_saved


def save_structure_analysis_excel(structure_dict, output_dir):
    """Save detailed bond information and statistics for structures to
    Excel."""
    data = []
    structure_list = []

    # Populate the data list with structured data from the dictionary
    for structure, info in structure_dict.items():
        first_formula = info["formulas"][0] if info["formulas"] else "N/A"
        structure_list.append(structure)

        first_row = True
        for bond_type, bond_info in info["bond_data"].items():
            row = [
                first_formula if first_row else "",
                structure if first_row else "",
                bond_type,
                bond_info["unique_bond_count"],
                bond_info["total_bond_count"],
                bond_info["avg_bond_length"],
                (
                    bond_info.get("std_dev_bond_length", 0)
                    if not np.isnan(bond_info.get("std_dev_bond_length", 0))
                    else 0
                ),
                (
                    bond_info.get("variance_bond_length", 0)
                    if not np.isnan(bond_info.get("variance_bond_length", 0))
                    else 0
                ),
            ]
            data.append(row)
            first_row = False

        # Add an empty row to visually separate structures
        data.append([""] * 8)  # Assuming there are 8 columns

    # Create a DataFrame
    df = pd.DataFrame(
        data,
        columns=[
            "Formula",
            "Structure Type",
            "Bond Type",
            "Unique Bond Count",
            "Total Bond Count",
            "Average Bond Length",
            "Standard Deviation",
            "Variance",
        ],
    )

    # Save DataFrame to an Excel file
    output_file_path = join(output_dir, "system_analysis_main.xlsx")
    df.to_excel(output_file_path, index=False)
    prompt_file_saved(output_file_path)
    # print(df.head(40))


def save_bond_overview_excel(structure_dict, possible_bond_pairs, output_dir):
    """Compile and save an overview of bond counts and types for
    structures to Excel."""
    bond_types = [f"{pair[0]}-{pair[1]}" for pair in possible_bond_pairs]

    # Initialize structure bond counts
    unique_structure_bond_counts = {bond: 0 for bond in bond_types}

    data = []
    file_to_structure = {}
    unique_structure_bond_counts = {bond: 0 for bond in bond_types}

    for structure, info in structure_dict.items():
        # Initialize structure-level bond counts
        if structure not in unique_structure_bond_counts:
            for bond in bond_types:
                unique_structure_bond_counts[bond] += (
                    info["bond_data"].get(bond, {}).get("unique_bond_count", 0)
                )

        for file in info.get("files", []):
            if file not in file_to_structure:
                file_to_structure[file] = {
                    "Structure": structure,
                    **{bond: 0 for bond in bond_types},
                }

            for bond_type, bond_info in info["bond_data"].items():
                bond_count = bond_info.get("unique_bond_count", 0)
                file_to_structure[file][bond_type] += bond_count

    for file, bond_counts in file_to_structure.items():
        row = [file, bond_counts.pop("Structure")] + [
            bond_counts[bond] for bond in bond_types
        ]
        data.append(row)

    # Calculate total bond counts across all files
    total_bonds = {
        bond: sum(file_to_structure[file][bond] for file in file_to_structure)
        for bond in bond_types
    }
    total_row = ["", "All files"] + [total_bonds[bond] for bond in bond_types]
    data.append(total_row)

    # Use already summed unique structure bond counts
    unique_total_row = ["", "Unique structures"] + [
        unique_structure_bond_counts[bond] for bond in bond_types
    ]
    data.append(unique_total_row)

    # Add bond fraction rows
    unique_total_bonds = {
        bond: unique_structure_bond_counts[bond] for bond in bond_types
    }
    total_unique_bonds = sum(unique_total_bonds.values())
    bond_fractions = [
        (
            unique_total_bonds[bond] / total_unique_bonds
            if total_unique_bonds > 0
            else 0
        )
        for bond in bond_types
    ]

    bond_fractions = np.around(bond_fractions, 3).tolist()
    bond_fraction_row = [
        "",
        "Bond fraction",
    ] + bond_fractions

    data.append(bond_fraction_row)

    columns = ["Entry", "Structure"] + bond_types
    df = pd.DataFrame(data, columns=columns)

    output_file_path = join(output_dir, "system_analysis_files.xlsx")
    df.to_excel(output_file_path, index=False)
    prompt_file_saved(output_file_path)
    # print(df.head(20))
