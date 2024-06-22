from core.run import coordination_analysis as CA
import pytest


@pytest.mark.slow
def test_coordination_analysis_run():
    dir_path = "20240616_cifkit_test"
    include_nested_files = False
    CA.process_each_folder(dir_path, include_nested_files)
