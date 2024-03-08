#conftest.py
import pytest
import preprocess.cif_parser_handler as cif_parser_handler

@pytest.fixture
def get_cif_527000_loop_values():
    CIF_loop_values = cif_parser_handler.get_CIF_loop_values(
        "tests/filter/cifs/527000.cif"
    )
    return CIF_loop_values


@pytest.fixture
def get_cif_1803318_loop_values():
    CIF_loop_values = cif_parser_handler.get_CIF_loop_values(
        "tests/filter/cifs/1803318.cif"
    )
    return CIF_loop_values


# Full occupancy
@pytest.fixture
def get_cif_300160_loop_values():
    CIF_loop_values = cif_parser_handler.get_CIF_loop_values(
        "tests/filter/cifs/300160.cif"
    )
    return CIF_loop_values