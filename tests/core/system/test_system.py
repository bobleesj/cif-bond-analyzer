import pytest
from cifkit import CifEnsemble
from core.run.system_analysis import conduct_system_analysis


@pytest.mark.slow
def test_conduct_system_analysis_nested():
    top_dir_path = "tests/data/system/excel"
    cif_ensemble_with_nested = CifEnsemble(top_dir_path, True)
    conduct_system_analysis(top_dir_path, cif_ensemble_with_nested)
    assert False


@pytest.mark.slow
def test_conduct_system_analysis_binary():
    top_dir_path = "tests/data/system/20240611_binary_2_unique_elements"
    cif_ensemble_with_nested = CifEnsemble(top_dir_path)
    conduct_system_analysis(top_dir_path, cif_ensemble_with_nested)
    assert False


@pytest.mark.slow
def test_conduct_system_analysis_ternary():
    top_dir_path = "tests/data/system/20240612_ternary_only"
    cif_ensemble_with_nested = CifEnsemble(top_dir_path)
    conduct_system_analysis(top_dir_path, cif_ensemble_with_nested)
    assert False


@pytest.mark.now
def test_conduct_system_analysis_ternary():
    top_dir_path = "tests/data/system/20240611_ternary_binary_combined"
    cif_ensemble_with_nested = CifEnsemble(top_dir_path)
    conduct_system_analysis(top_dir_path, cif_ensemble_with_nested)
    assert False
