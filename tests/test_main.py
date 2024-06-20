from run import system_analysis, coordination
import pytest


@pytest.mark.slow
def test_20240611_binary_2_unique_elements():
    # 20240611_binary_2_unique_elements
    dir_path = "tests/data/20240611_binary_2_unique_elements"
    system_analysis.generate_site_data(dir_path)
    system_analysis.conduct_system_analysis(dir_path)
    coordination.process_each_folder(dir_path)


@pytest.mark.slow
def test_20240611_binary_3_unique_elements():
    # 20240611_binary_3_unique_elements
    dir_path = "tests/data/20240611_binary_3_unique_elements"
    system_analysis.generate_site_data(dir_path)
    system_analysis.conduct_system_analysis(dir_path)
    coordination.process_each_folder(dir_path)


@pytest.mark.now
def test_20240611_ternary_binary_combined():
    # 20240611_ternary_binary_combined
    dir_path = "tests/data/20240611_ternary_binary_combined"
    # system_analysis.generate_site_data(dir_path)
    system_analysis.conduct_system_analysis(dir_path)
    # coordination.process_each_folder(dir_path)


@pytest.mark.slow
def test_20240612_ternary_only():
    # 20240612_ternary_only
    dir_path = "tests/data/20240612_ternary_only"
    system_analysis.generate_site_data(dir_path)
    system_analysis.conduct_system_analysis(dir_path)
    coordination.process_each_folder(dir_path)


@pytest.mark.slow
def test_20240531_ErCoIn_ternary_binary():
    # 20240531_ErCoIn_ternary_binary (~160 files)
    dir_path = "tests/data/20240531_ErCoIn_ternary_binary"
    system_analysis.generate_site_data(dir_path)
    system_analysis.conduct_system_analysis(dir_path)
    coordination.process_each_folder(dir_path)
