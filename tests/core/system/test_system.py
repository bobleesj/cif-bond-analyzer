import os
import pytest
from cifkit import CifEnsemble
from core.run.system_analysis import conduct_system_analysis
from cifkit.utils.folder import check_file_exists
import shutil

# @pytest.mark.now
# def test_conduct_system_analysis_binary():
#     dir_path = "tests/data/system/20240611_binary_2_unique_elements"
#     conduct_system_analysis(dir_path)


# @pytest.mark.now
# def test_conduct_system_analysis_nested():
#     dir_path = "tests/data/system/20240621_nested_binary_2_unique_elements"
#     conduct_system_analysis(dir_path)


# @pytest.mark.now
# def test_conduct_system_analysis_ternary():
#     dir_path = "tests/data/system/20240612_ternary_only"
#     conduct_system_analysis(dir_path)


# @pytest.mark.now
# def test_conduct_system_analysis_ternary_binary_combined():
#     dir_path = "tests/data/system/20240611_ternary_binary_combined"
#     conduct_system_analysis(dir_path)


# @pytest.mark.now
# def test_conduct_system_analysis_ternary_binary_combined_big():
#     dir_path = "tests/data/system/20240611_binary_3_unique_elements"
#     conduct_system_analysis(dir_path)
#     # assert False


@pytest.mark.now
def test_conduct_system_analysis_ternary_binary_combined_big():
    base_dir = "tests/data/system/20240531_ErCoIn_ternary_binary"
    output_dir = os.path.join(base_dir, "output", "system_analysis")
    is_CN_used = False
    use_existing_json = True
    conduct_system_analysis(base_dir, is_CN_used, use_existing_json)

    required_files = [
        "color_map_overall.png",
        "ternary.png",
        "composite_ternary_1.png",
        "composite_binary_2.png",
    ]

    for file_name in required_files:
        file_path = os.path.join(output_dir, file_name)
        assert check_file_exists(file_path)

    shutil.rmtree(os.path.join(base_dir, "output"))
