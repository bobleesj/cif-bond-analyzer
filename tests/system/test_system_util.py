import pytest
from postprocess.system.system_util import (
    get_is_single_binary,
    get_is_double_binary,
    get_is_ternary,
    get_is_binary_ternary_combined,
)


@pytest.mark.fast
def test_get_is_single_binary(is_single_binary_json_path):
    json_file_path = is_single_binary_json_path
    assert get_is_single_binary(json_file_path) == True
    assert get_is_double_binary(json_file_path) == False
    assert get_is_ternary(json_file_path) == False
    assert (
        get_is_binary_ternary_combined(json_file_path)
        == False
    )


@pytest.mark.fast
def test_get_is_double_binary(is_double_binary_json_path):
    json_file_path = is_double_binary_json_path
    assert get_is_double_binary(json_file_path) == True
    assert get_is_single_binary(json_file_path) == False
    assert get_is_ternary(json_file_path) == False
    assert (
        get_is_binary_ternary_combined(json_file_path)
        == False
    )


@pytest.mark.fast
def test_get_is_binary_ternary_combined(
    is_binary_ternary_combined_json_path,
):
    json_file_path = is_binary_ternary_combined_json_path
    assert (
        get_is_binary_ternary_combined(json_file_path)
        == True
    )
    assert get_is_single_binary(json_file_path) == False
    assert get_is_double_binary(json_file_path) == False
    assert get_is_ternary(json_file_path) == False


@pytest.mark.fast
def test_is_ternary(is_ternary_json_path):
    json_file_path = is_ternary_json_path
    assert get_is_ternary(json_file_path) == True
    assert (
        get_is_binary_ternary_combined(json_file_path)
        == False
    )
    assert get_is_single_binary(json_file_path) == False
    assert get_is_double_binary(json_file_path) == False
