from util import folder
from run import system_analysis
import pytest


@pytest.mark.slow
def test_system_analysis():
    # 20240611_binary_2_unique_elements
    dir_path = "tests/system/data/20240611_binary_2_unique_elements"
    system_analysis.generate_site_data(dir_path)
    system_analysis.conduct_system_analysis(dir_path)

    # 20240611_binary_3_unique_elements
    dir_path = "tests/system/data/20240611_binary_3_unique_elements"
    system_analysis.generate_site_data(dir_path)
    system_analysis.conduct_system_analysis(dir_path)

    # 20240611_ternary_binary_combined
    dir_path = "tests/system/data/20240611_ternary_binary_combined"
    system_analysis.generate_site_data(dir_path)
    system_analysis.conduct_system_analysis(dir_path)

    # 20240612_ternary_only
    dir_path = "tests/system/data/20240612_ternary_only"
    system_analysis.generate_site_data(dir_path)
    system_analysis.conduct_system_analysis(dir_path)

    # 20240531_ErCoIn_ternary_binary (~160 files)
    dir_path = "tests/system/data/20240531_ErCoIn_ternary_binary"
    system_analysis.generate_site_data(dir_path)
    system_analysis.conduct_system_analysis(dir_path)
