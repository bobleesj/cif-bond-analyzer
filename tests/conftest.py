# conftest.py
import pytest
from preprocess import cif_parser_handler


@pytest.fixture
def get_cif_527000_loop_values():
    CIF_loop_values = (
        cif_parser_handler.get_cif_loop_values(
            "tests/filter/cifs/527000.cif"
        )
    )
    return CIF_loop_values


@pytest.fixture
def get_cif_1803318_loop_values():
    CIF_loop_values = (
        cif_parser_handler.get_cif_loop_values(
            "tests/filter/cifs/1803318.cif"
        )
    )
    return CIF_loop_values


@pytest.fixture
def get_cif_300160_loop_values():
    CIF_loop_values = (
        cif_parser_handler.get_cif_loop_values(
            "tests/filter/cifs/300160.cif"
        )
    )
    return CIF_loop_values


@pytest.fixture
def get_cif_1831432_loop_values():
    CIF_loop_values = (
        cif_parser_handler.get_cif_loop_values(
            "tests/filter/cifs/1831432.cif"
        )
    )
    return CIF_loop_values


@pytest.fixture
def get_cif_529848_loop_values():
    CIF_loop_values = (
        cif_parser_handler.get_cif_loop_values(
            "tests/filter/cifs/529848.cif"
        )
    )
    return CIF_loop_values


@pytest.fixture
def get_cif_1617211_loop_values():
    CIF_loop_values = (
        cif_parser_handler.get_cif_loop_values(
            "tests/filter/cifs/1617211.cif"
        )
    )
    return CIF_loop_values


@pytest.fixture
def get_cif_URhIn_loop_values():
    CIF_loop_values = (
        cif_parser_handler.get_cif_loop_values(
            "tests/filter/cifs/URhIn.cif"
        )
    )
    return CIF_loop_values


"""
Test system analysis
"""


@pytest.fixture
def is_single_binary_json_path():
    return "tests/system/data/binary_single_type/binary_single_type.json"


@pytest.fixture
def is_double_binary_json_path():
    return (
        "tests/system/data/binary_double_type/updated.json"
    )


@pytest.fixture
def is_binary_ternary_combined_json_path():
    return "tests/system/data/binary_ternary_combined_type/updated.json"


@pytest.fixture
def is_ternary_json_path():
    return "tests/system/data/ternary_type/ternary.json"
