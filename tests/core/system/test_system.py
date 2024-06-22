import pytest
from cifkit import CifEnsemble
from core.run.system_analysis import conduct_system_analysis


@pytest.mark.now
def test_conduct_system_analysis_binary():
    dir_path = "tests/data/system/20240611_binary_2_unique_elements"
    conduct_system_analysis(dir_path)
    assert False


@pytest.mark.now
def test_conduct_system_analysis_nested():
    dir_path = "tests/data/system/20240621_nested_binary_2_unique_elements"
    conduct_system_analysis(dir_path)


@pytest.mark.now
def test_conduct_system_analysis_ternary():
    dir_path = "tests/data/system/20240612_ternary_only"
    conduct_system_analysis(dir_path)


@pytest.mark.now
def test_conduct_system_analysis_ternary_binary_combined():
    dir_path = "tests/data/system/20240611_ternary_binary_combined"
    conduct_system_analysis(dir_path)
    assert False


@pytest.mark.now
def test_conduct_system_analysis_ternary_binary_combined_big():
    dir_path = "tests/data/system/20240611_binary_3_unique_elements"
    conduct_system_analysis(dir_path)
    # assert False


@pytest.mark.now
def test_conduct_system_analysis_ternary_binary_combined_big():
    dir_path = "tests/data/system/20240531_ErCoIn_ternary_binary"
    conduct_system_analysis(dir_path)
