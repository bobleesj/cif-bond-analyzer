import pytest
from cifkit.utils.folder import check_file_exists
from core.run.site_analysis import generate_site_analysis_data
import json
import shutil
from os.path import join
from jsondiff import diff


@pytest.fixture
def paths():
    base_path = "tests/data/no_json/20240611_ternary_binary_combined"
    output_path = join(base_path, "output")
    site_json_path = join(
        output_path,
        "20240611_ternary_binary_combined_site_pairs.json",
    )

    return base_path, output_path, site_json_path


def check_files_exists(output_path):
    files_to_check = [
        "summary_element.txt",
        "20240611_ternary_binary_combined_element_pairs.json",
        "20240611_ternary_binary_combined_element_pairs.xlsx",
        "20240611_ternary_binary_combined_site_pairs.json",
        "20240611_ternary_binary_combined_site_pairs.xlsx",
        "histogram_element_pair_1.png",
        "histogram_site_pair_1.png",
        "single_histogram/histogram_element_pair/Er-Co.png",
        "single_histogram/histogram_site_pair/Er-Co.png",
    ]

    # Check each file in the list
    for file_name in files_to_check:
        file_path = join(output_path, file_name)
        assert check_file_exists(file_path)


@pytest.mark.slow
def test_run_site_without_nested_files(paths):
    base_path, output_path, site_json_path = paths
    add_nested_files = False
    generate_site_analysis_data(base_path, add_nested_files)

    # Define expected JSON data
    expected_data = {
        "Er-Co": {
            "1956508": [
                {
                    "dist": 2.799,
                    "mixing": "full_occupancy",
                    "formula": "Er3Co1.87In4",
                    "tag": "",
                    "structure": "Lu3Co2In4",
                }
            ]
        },
        "Co-In": {
            "1956508": [
                {
                    "dist": 2.687,
                    "mixing": "deficiency_without_atomic_mixing",
                    "formula": "Er3Co1.87In4",
                    "tag": "",
                    "structure": "Lu3Co2In4",
                }
            ],
            "1300872_bi": [
                {
                    "dist": 2.615,
                    "mixing": "full_occupancy",
                    "formula": "CoIn3",
                    "tag": "",
                    "structure": "IrIn3",
                },
                {
                    "dist": 2.6,
                    "mixing": "full_occupancy",
                    "formula": "CoIn3",
                    "tag": "",
                    "structure": "IrIn3",
                },
            ],
        },
        "In-In": {
            "1956508": [
                {
                    "dist": 2.949,
                    "mixing": "full_occupancy",
                    "formula": "Er3Co1.87In4",
                    "tag": "",
                    "structure": "Lu3Co2In4",
                }
            ]
        },
    }

    # Read actual JSON data from file and compare
    with open(site_json_path, "r") as file:
        actual_data = json.load(file)
        differences = diff(actual_data, expected_data)
        assert (
            not differences
        ), f"JSON data does not match expected structure: {differences}"
    # Cleanup
    check_files_exists(output_path)
    shutil.rmtree(output_path)


@pytest.mark.slow
def test_run_site_with_nested_files(paths):
    base_path, output_path, json_path = paths
    add_nested_files = True
    generate_site_analysis_data(base_path, add_nested_files)

    # Define expected JSON data
    expected_data = {
        "Er-Co": {
            "1956508": [
                {
                    "dist": 2.799,
                    "mixing": "full_occupancy",
                    "formula": "Er3Co1.87In4",
                    "tag": "",
                    "structure": "Lu3Co2In4",
                }
            ],
            "250361": [
                {
                    "dist": 2.966,
                    "mixing": "full_occupancy",
                    "formula": "ErCo2",
                    "tag": "rt",
                    "structure": "MgCu2",
                }
            ],
        },
        "Co-In": {
            "1956508": [
                {
                    "dist": 2.687,
                    "mixing": "deficiency_without_atomic_mixing",
                    "formula": "Er3Co1.87In4",
                    "tag": "",
                    "structure": "Lu3Co2In4",
                }
            ],
            "1300872_bi": [
                {
                    "dist": 2.615,
                    "mixing": "full_occupancy",
                    "formula": "CoIn3",
                    "tag": "",
                    "structure": "IrIn3",
                },
                {
                    "dist": 2.6,
                    "mixing": "full_occupancy",
                    "formula": "CoIn3",
                    "tag": "",
                    "structure": "IrIn3",
                },
            ],
            "451623_bi": [
                {
                    "dist": 2.735,
                    "mixing": "full_occupancy",
                    "formula": "CoIn2",
                    "tag": "",
                    "structure": "Mg2Cu",
                },
                {
                    "dist": 2.682,
                    "mixing": "full_occupancy",
                    "formula": "CoIn2",
                    "tag": "",
                    "structure": "Mg2Cu",
                },
            ],
        },
        "In-In": {
            "1956508": [
                {
                    "dist": 2.949,
                    "mixing": "full_occupancy",
                    "formula": "Er3Co1.87In4",
                    "tag": "",
                    "structure": "Lu3Co2In4",
                }
            ]
        },
        "Co-Co": {
            "250361": [
                {
                    "dist": 2.529,
                    "mixing": "full_occupancy",
                    "formula": "ErCo2",
                    "tag": "rt",
                    "structure": "MgCu2",
                }
            ]
        },
    }

    # Read actual JSON data from file and compare
    with open(json_path, "r") as file:
        actual_data = json.load(file)

        differences = diff(actual_data, expected_data)
        assert not differences

    # Cleanup
    check_files_exists(output_path)
    shutil.rmtree(output_path)
