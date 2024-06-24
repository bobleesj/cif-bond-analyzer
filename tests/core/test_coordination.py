import os
import json
import shutil
from core.run import coordination_analysis as CA
from cifkit.utils.folder import check_file_exists
import pytest
from os.path import join


@pytest.fixture
def paths():
    base_dir = "tests/data/no_json/20240611_binary_2_unique_elements"
    output_path = join(base_dir, "output")
    json_path = join(output_path, "coordination", "CN_connections.json")
    excel_path = join(output_path, "coordination", "CN_connections.xlsx")
    return base_dir, output_path, json_path, excel_path


def assert_json_key(json_path, expected_count) -> bool:
    with open(json_path, "r") as file:
        data = json.load(file)
    return len(data.keys()) == expected_count


@pytest.mark.slow
def test_coordination_analysis_run(paths):
    base_dir, output_path, json_path, excel_path = paths
    include_nested_files = False
    CA.process_each_folder(base_dir, include_nested_files)
    assert assert_json_key(json_path, 2)
    assert check_file_exists(excel_path)
    shutil.rmtree(output_path)


@pytest.mark.slow
def test_coordination_analysis_run_nested_files(paths):
    include_nested_files = True
    base_dir, output_path, json_path, excel_path = paths
    CA.process_each_folder(base_dir, include_nested_files)
    assert assert_json_key(json_path, 4)
    assert check_file_exists(excel_path)
    shutil.rmtree(output_path)
