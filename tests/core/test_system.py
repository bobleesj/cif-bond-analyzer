import os
import pytest
from os.path import join
from core.run.system_analysis import conduct_system_analysis
from cifkit.utils.folder import check_file_exists
import shutil


def check_files_exists(output_path, required_files):
    # Check each file in the list
    for file_name in required_files:
        file_path = join(output_path, file_name)
        assert check_file_exists(file_path)


"""
Use existing JSON, no CN
"""


@pytest.mark.slow
def test_SA_ternary_binary_combined_big_use_json():
    base_dir = "tests/data/with_json/20240623_ErCoIn_nested"
    SA_dir = os.path.join(base_dir, "output", "system_analysis")
    is_CN_used = False
    use_existing_json = True
    conduct_system_analysis(base_dir, is_CN_used, use_existing_json)

    required_files = [
        "color_map_overall.png",
        "color_map_Co-Co.png",
        "color_map_Co-In.png",
        "composite_binary_1.png",
        "composite_binary_2.png",
        "composite_ternary_1.png",
        "system_analysis_files.xlsx",
        "system_analysis_main.xlsx",
        "ternary.png",
    ]

    check_files_exists(SA_dir, required_files)
    shutil.rmtree(SA_dir)


@pytest.mark.slow
def test_SA_binary_2_unique_elements_use_json():
    base_dir = "tests/data/with_json/20240611_binary_2_unique_elements"
    SA_dir = os.path.join(base_dir, "output", "system_analysis")
    is_CN_used = False
    use_existing_json = True
    conduct_system_analysis(base_dir, is_CN_used, use_existing_json)

    required_files = [
        "composite_binary_1.png",
        "binary_single.png",
        "system_analysis_files.xlsx",
        "system_analysis_main.xlsx",
    ]
    check_files_exists(SA_dir, required_files)


@pytest.mark.slow
def test_SA_ternary_only_use_json():
    base_dir = "tests/data/with_json/20240612_ternary_only"
    SA_dir = os.path.join(base_dir, "output", "system_analysis")
    is_CN_used = False
    use_existing_json = True
    conduct_system_analysis(base_dir, is_CN_used, use_existing_json)

    required_files = [
        "color_map_overall.png",
        "color_map_Co-Co.png",
        "color_map_Er-Er.png",
        "composite_ternary_1.png",
        "system_analysis_files.xlsx",
        "system_analysis_main.xlsx",
        "ternary.png",
    ]
    check_files_exists(SA_dir, required_files)


"""
Use CN
"""


@pytest.mark.slow
def test_SA_ternary_binary_combined_big_use_CN():
    base_dir = "tests/data/no_json/20240611_ternary_binary_combined"
    SA_dir = os.path.join(base_dir, "output", "system_analysis")
    is_CN_used = True
    conduct_system_analysis(base_dir, is_CN_used, False)

    required_files = [
        "color_map_Co-Co_CN.png",
        "color_map_overall_CN.png",
        "composite_binary_1_CN.png",
        "composite_ternary_1_CN.png",
        "ternary_CN.png",
        "system_analysis_files.xlsx",
        "system_analysis_main.xlsx",
    ]

    check_files_exists(SA_dir, required_files)
    shutil.rmtree(SA_dir)


@pytest.mark.slow
def test_SA_binary_2_unique_elements_use_CN():
    base_dir = "tests/data/no_json/20240611_binary_2_unique_elements"
    SA_dir = os.path.join(base_dir, "output", "system_analysis")
    is_CN_used = True
    conduct_system_analysis(base_dir, is_CN_used, False)

    required_files = [
        "composite_binary_1_CN.png",
        "binary_single_CN.png",
        "system_analysis_files.xlsx",
        "system_analysis_main.xlsx",
    ]
    check_files_exists(SA_dir, required_files)
    shutil.rmtree(SA_dir)


@pytest.mark.slow
def test_SA_ternary_only_use_CN():
    base_dir = "tests/data/no_json/20240612_ternary_only"
    SA_dir = os.path.join(base_dir, "output", "system_analysis")
    is_CN_used = True
    conduct_system_analysis(base_dir, is_CN_used, False)

    required_files = [
        "color_map_overall_CN.png",
        "color_map_Co-Co_CN.png",
        "color_map_Er-Er_CN.png",
        "composite_ternary_1_CN.png",
        "system_analysis_files.xlsx",
        "system_analysis_main.xlsx",
        "ternary_CN.png",
    ]
    check_files_exists(SA_dir, required_files)
