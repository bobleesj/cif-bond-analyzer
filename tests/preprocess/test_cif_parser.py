import pytest
import preprocess.cif_parser as cif_parser


@pytest.mark.fast
def test_get_unique_element_list(
    get_cif_527000_loop_values,
):
    CIF_loop_values = get_cif_527000_loop_values

    unique_element_list = cif_parser.get_unique_element_list(CIF_loop_values)
    assert set(unique_element_list) == set(["Rh", "Si"])


@pytest.mark.fast
def test_get_atom_label_list(get_cif_527000_loop_values):
    CIF_loop_values = get_cif_527000_loop_values

    label_list = cif_parser.get_atom_label_list(CIF_loop_values)
    assert label_list == ["Rh2", "Si", "Rh1"]


@pytest.mark.fast
def test_get_num_of_atom_labels(get_cif_527000_loop_values):
    CIF_loop_values = get_cif_527000_loop_values

    num_of_atom_labels = cif_parser.get_num_of_atom_labels(CIF_loop_values)
    assert num_of_atom_labels == 3
