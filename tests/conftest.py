# conftest.py
import pytest

"""
Test system analysis
"""


@pytest.fixture
def is_single_binary_json_path():
    return "tests/data/binary_single_type/binary_single_type.json"


@pytest.fixture
def is_double_binary_json_path():
    return "tests/data/binary_double_type/updated.json"


@pytest.fixture
def is_binary_ternary_combined_json_path():
    return "tests/data/binary_ternary_combined_type/updated.json"


@pytest.fixture
def is_ternary_json_path():
    return "tests/data/ternary_type/ternary.json"
