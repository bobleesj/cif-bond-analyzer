from util import prompt
from run.coordination import get_CN_connections, get_CN_bond_fractions_sorted
import pytest


@pytest.mark.fast
def test_process_single_file():
    file_path = "tests/coordination/data/Er3Co2In4.cif"
    connections_CN = get_CN_connections(file_path)
    bond_fracitons = get_CN_bond_fractions_sorted(connections_CN)
    assert bond_fracitons == {
        ("Er", "Er"): 0.065,
        ("Er", "Co"): 0.194,
        ("Co", "Co"): 0.065,
        ("Co", "In"): 0.194,
        ("In", "In"): 0.161,
        ("Er", "In"): 0.323,
    }
    assert False
