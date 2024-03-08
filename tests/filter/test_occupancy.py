import pytest
import filter.occupancy as occupancy
import preprocess.cif_parser_handler as cif_parser_handler


@pytest.mark.fast
def test_get_atom_site_mixing_info(get_cif_527000_loop_values):
    atom_mixing_type = occupancy.get_atom_site_mixing_info(
        get_cif_527000_loop_values
    )
    assert atom_mixing_type == "3"

@pytest.mark.fast
def test_get_atom_site_mixing_info(get_cif_1803318_loop_values):
    atom_mixing_type = occupancy.get_atom_site_mixing_info(
        get_cif_1803318_loop_values
    )
    assert atom_mixing_type == "4"


@pytest.mark.fast
def test_get_all_possible_ordered_label_pair_tuples(
        get_cif_300160_loop_values):

    atom_site_mixing_file_info = occupancy.get_atom_site_mixing_info(
        get_cif_300160_loop_values
    )

    ordered_label_pairs = occupancy.get_all_possible_ordered_label_pairs(
        get_cif_300160_loop_values
    )
    assert len(ordered_label_pairs) == 6
    assert sorted(ordered_label_pairs) == sorted([
        ("Rh1", "Rh1"),
        ("Ge1", "Ge1"),
        ("Sm1", "Sm1"),
        ("Sm1", "Rh1"),
        ("Sm1", "Ge1"),
        ("Rh1", "Ge1")
        ])


@pytest.mark.now
def test_get_atom_site_mixing_dict_type_4(get_cif_300160_loop_values):
    atom_site_mixing_file_info = occupancy.get_atom_site_mixing_info(
        get_cif_300160_loop_values
    )

    atom_site_pair_dict = occupancy.get_atom_site_mixing_dict(
        atom_site_mixing_file_info,
        get_cif_300160_loop_values
    )

    # Mendeleev # - Ge 79, Rh 59, Sm 23
    assert len(atom_site_pair_dict) == 6
    assert atom_site_pair_dict[("Rh1", "Rh1")] == "4"
    assert atom_site_pair_dict[("Ge1", "Ge1")] == "4"
    assert atom_site_pair_dict[("Sm1", "Sm1")] == "4"
    assert atom_site_pair_dict[("Sm1", "Rh1")] == "4"
    assert atom_site_pair_dict[("Sm1", "Ge1")] == "4"
    assert atom_site_pair_dict[("Rh1", "Ge1")] == "4"


@pytest.mark.now
def test_get_atom_site_mixing_dict_type_3(get_cif_527000_loop_values):
    atom_site_mixing_file_info = occupancy.get_atom_site_mixing_info(
        get_cif_527000_loop_values
    )

    atom_site_pair_dict = occupancy.get_atom_site_mixing_dict(
        atom_site_mixing_file_info,
        get_cif_527000_loop_values
    )

    # Mendeleev # - Rh 59, Si 78
    assert len(atom_site_pair_dict) == 6
    assert atom_site_pair_dict[("Rh1", "Si")] == "4"
    assert atom_site_pair_dict[("Rh1", "Rh1")] == "4"
    assert atom_site_pair_dict[("Rh1", "Rh2")] == "3"
    assert atom_site_pair_dict[("Rh2", "Rh2")] == "3"
    assert atom_site_pair_dict[("Si", "Si")] == "4"
    assert atom_site_pair_dict[("Rh2", "Si")] == "3"


    '''
    if is_atomic_mixing and not is_full_occupancy:
        # "deficiency"
        return "1"

    elif is_atomic_mixing and is_full_occupancy:
        # "full_occupancy_atomic_mixing"
        return "2"

    elif not is_atomic_mixing and not is_full_occupancy:
        # "deficiency_no_atomic_mixing"
        return "3"

    elif is_full_occupancy:
        # "full_occupancy"
        return "4"
        
    527000
    assert atom_site_pair_dict["Rh2-Si"] == "3"
    assert atom_site_pair_dict["Rh1-Rh1"] == "4"
    # We need to sort using Mendeleev number
    Rh - 59
    Si - 78
    Pair: Rh2-Si 2.28 Å - deficiency_no_atomic_mixing
    Pair: Rh1-Rh1 2.524 Å - full_occupancy
    '''
