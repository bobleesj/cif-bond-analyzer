from main import main  # Assuming main.py and this test file are in the same directory
import os
import json
import util.folder as folder
import pytest


def cleanup(dir_path):
    csv_dir_path = os.path.join(dir_path, "csv")
    output_dir_path = os.path.join(dir_path, "output")
    folder.remove_directories([csv_dir_path, output_dir_path])

def run_test(dir_path, expected_json):
    cif_folder_name = os.path.basename(dir_path)
    output_dir_path = os.path.join(dir_path, "output")
    json_output_path = os.path.join(output_dir_path, f"{cif_folder_name}_pairs.json")

    # Run
    main(False, dir_path)
    
    # Load output
    with open(json_output_path, 'r') as file:
        actual_output = json.load(file)

    # Test
    assert actual_output == expected_json, "Output JSON does not match expected output."

@pytest.mark.slow
def test_cif_json_processing():
    test_cases = [
        ("tests/single_cif_file_test/1803318", {
            "In-In": [{"File": "1803318.cif", "Distance": 2.999, "Atomic Site": "full_occupancy"}],
            "Er-Co": [{"File": "1803318.cif", "Distance": 2.644, "Atomic Site": "full_occupancy"}],
            "Er-Er": [{"File": "1803318.cif", "Distance": 3.34, "Atomic Site": "full_occupancy"}],
            "Er-In": [{"File": "1803318.cif", "Distance": 3.024, "Atomic Site": "full_occupancy"}]
        }),
        ("tests/single_cif_file_test/539016", {
            "Ga-Ga": [{"File": "539016.cif", "Distance": 2.358, "Atomic Site": "full_occupancy_atomic_mixing"}],
            "La-Ga": [{"File": "539016.cif", "Distance": 3.291, "Atomic Site": "full_occupancy_atomic_mixing"}],
            "Co-Ga": [{"File": "539016.cif", "Distance": 2.601, "Atomic Site": "full_occupancy_atomic_mixing"}]
        }),
        ("tests/single_cif_file_test/560709", {
            "Co-Ga": [{"File": "560709.cif", "Distance": 2.501, "Atomic Site": "full_occupancy_atomic_mixing"}],
            "Co-Co": [{"File": "560709.cif", "Distance": 2.501, "Atomic Site": "full_occupancy_atomic_mixing"}],
            "Ga-Ga": [{"File": "560709.cif", "Distance": 2.501, "Atomic Site": "full_occupancy_atomic_mixing"}],
            "La-Co": [{"File": "560709.cif", "Distance": 2.979, "Atomic Site": "full_occupancy_atomic_mixing"}],
            "La-Ga": [{"File": "560709.cif", "Distance": 2.979, "Atomic Site": "full_occupancy_atomic_mixing"}],
        })
    ]

    for dir_path, expected_json in test_cases:
        # cleanup(dir_path)  # Cleanup before each test
        run_test(dir_path, expected_json)
        # cleanup(dir_path)  # Cleanup after each test

# Main execution
if __name__ == "__main__":
    test_cif_json_processing()
