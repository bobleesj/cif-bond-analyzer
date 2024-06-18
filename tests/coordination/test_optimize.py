from util import prompt
from run.coordination import (
    get_CN_connections,
    get_CN_bond_fractions_sorted,
)
import pytest


@pytest.mark.fast
def test_process_single_file():
    file_path = "tests/coordination/data/URhIn.cif"
    connections_CN = get_CN_connections(file_path)
    assert False
