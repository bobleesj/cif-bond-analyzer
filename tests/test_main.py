from run import bond
import os
import json
import pytest
import shutil
import tempfile
from deepdiff import DeepDiff


def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)


def compare_json_files(file1, file2):
    json1 = load_json(file1)
    json2 = load_json(file2)
    diff = DeepDiff(json1, json2, ignore_order=True)
    assert not diff, f"JSON files are different: {diff}"


def run_test_for_directory(cif_dir):
    """
    Run integration test for a given CIF directory.

    This function sets up a temporary directory, executes the main function
    to process the CIF files, and then compares the output JSON files
    """
    temp_dir = tempfile.mkdtemp()
    temp_cif_dir = os.path.join(temp_dir, os.path.basename(cif_dir))
    shutil.copytree(cif_dir, temp_cif_dir)
    script_path = ""
    bond.run_bond(
        script_path,
        is_iteractive_mode=False,
        given_dir_path=temp_cif_dir,
    )

    # Paths for expected and actual output files
    expected_element_pairs_file = os.path.join(
        cif_dir,
        "output",
        f"{os.path.basename(cif_dir)}_element_pairs.json",
    )
    expected_site_pairs_file = os.path.join(
        cif_dir,
        "output",
        f"{os.path.basename(cif_dir)}_site_pairs.json",
    )
    actual_element_pairs_file = os.path.join(
        temp_cif_dir,
        "output",
        f"{os.path.basename(cif_dir)}_element_pairs.json",
    )
    actual_site_pairs_file = os.path.join(
        temp_cif_dir,
        "output",
        f"{os.path.basename(cif_dir)}_site_pairs.json",
    )

    compare_json_files(expected_element_pairs_file, actual_element_pairs_file)
    compare_json_files(expected_site_pairs_file, actual_site_pairs_file)


@pytest.mark.fast
def test_1810929_NiGa():
    run_test_for_directory("tests/cif/1810929_NiGa")


@pytest.mark.fast
def test_1814810_ErCoIn():
    run_test_for_directory("tests/cif/1814810_ErCoIn")


# Main execution
if __name__ == "__main__":
    test_1810929_NiGa()
    test_1814810_ErCoIn()
