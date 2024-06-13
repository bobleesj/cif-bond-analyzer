from util import folder
from run import system_analysis
import pytest


@pytest.mark.slow
def test_system_analysis():
    # # 20240611_binary_2_unique_elements
    # dir_path = "tests/system/data/20240611_binary_2_unique_elements"
    # system_analysis.process_system_analysis_by_folder(dir_path)

    # # 20240611_binary_3_unique_elements
    # dir_path = "tests/system/data/20240611_binary_3_unique_elements"
    # system_analysis.process_system_analysis_by_folder(dir_path)

    # 20240611_ternary_binary_cobined
    dir_path = "tests/system/data/20240611_ternary_binary_combined"
    system_analysis.process_system_analysis_by_folder(dir_path)

    # # 20240612_ternary_only
    # dir_path = "tests/system/data/20240612_ternary_only"
    # system_analysis.process_system_analysis_by_folder(dir_path)
