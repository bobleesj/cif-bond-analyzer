import json
import os
from preprocess import cif_parser


def conduct_system_analysis():
    print("Hello world")

    # Specify the path to the JSON file
    json_file_path = "20240411_system_analysis/output/20240411_system_analysis_site_pairs.json"

    # Read the JSON file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Directory where .cif files are stored
    cif_directory = "20240411_system_analysis"

    # Process each key and its site pairs in the JSON
    for key, site_pairs in data.items():
        print(f"Processing data for: {key}")
        for site_id, pairs in site_pairs.items():
            cif_file_path = os.path.join(cif_directory, f"{site_id}.cif")

            if os.path.exists(cif_file_path):
                print(f"Processing {cif_file_path}")
                try:
                    # Load the CIF file
                    block = cif_parser.get_cif_block(cif_file_path)

                    # Extract and clean the desired fields
                    chemical_formula_structural = block.find_value(
                        "_chemical_formula_structural"
                    ).replace("~", "")
                    chemical_name_structure_type = (
                        block.find_value("_chemical_name_structure_type")
                        .split(",")[0]
                        .replace("~", "")
                    )

                    # Print or process the extracted and cleaned data
                    print(f"Formula Structural: {chemical_formula_structural}")
                    print(f"Structure Type: {chemical_name_structure_type}")
                    print()
                except Exception as e:
                    print(f"Failed to process {cif_file_path}: {e}")
            else:
                print(f"File not found: {cif_file_path}")


if __name__ == "__main__":
    conduct_system_analysis()
