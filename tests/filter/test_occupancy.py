import pytest
import filter.occupancy as occupancy
import preprocess.cif_parser_handler as cif_parser_handler


@pytest.mark.fast
def test_get_atom_site_mixing_info_1(get_cif_527000_loop_values):
    atom_mixing_type = occupancy.get_atom_site_mixing_info(
        get_cif_527000_loop_values
    )
    assert atom_mixing_type == "3"


@pytest.mark.fast
def test_get_atom_site_mixing_info_2(get_cif_1803318_loop_values):
    atom_mixing_type = occupancy.get_atom_site_mixing_info(
        get_cif_1803318_loop_values
    )
    assert atom_mixing_type == "4"


@pytest.mark.fast
def test_get_all_possible_ordered_label_pair_tuples_300160(
    get_cif_300160_loop_values,
):
    ordered_label_pairs = (
        occupancy.get_all_possible_ordered_label_pairs(
            get_cif_300160_loop_values
        )
    )
    assert len(ordered_label_pairs) == 6
    assert sorted(ordered_label_pairs) == sorted(
        [
            ("Rh1", "Rh1"),
            ("Ge1", "Ge1"),
            ("Sm1", "Sm1"),
            ("Sm1", "Rh1"),
            ("Sm1", "Ge1"),
            ("Rh1", "Ge1"),
        ]
    )


@pytest.mark.fast
def test_get_all_possible_ordered_label_pair_tuples_URhIn(
    get_cif_URhIn_loop_values,
):
    ordered_label_pairs = (
        occupancy.get_all_possible_ordered_label_pairs(
            get_cif_URhIn_loop_values
        )
    )

    # Mendelee # of U 20, Rh 59, In 75
    # In1, U1, Rh1, Rh2

    assert len(ordered_label_pairs) == 10
    assert sorted(ordered_label_pairs) == sorted(
        [
            ("In1", "In1"),
            ("U1", "U1"),
            ("Rh2", "Rh2"),
            ("Rh1", "Rh1"),  # 4 same pairs
            ("U1", "In1"),
            ("Rh1", "In1"),
            ("Rh2", "In1"),  # 3 pairs below In1
            ("Rh1", "Rh2"),
            ("U1", "Rh2"),  # 2 pairs below Rh2
            ("U1", "Rh1"),  # 1 pair below Rh1
        ]
    )


@pytest.mark.fast
def test_get_atom_site_mixing_dict_1(get_cif_300160_loop_values):
    atom_site_mixing_file_info = occupancy.get_atom_site_mixing_info(
        get_cif_300160_loop_values
    )

    atom_site_pair_dict = occupancy.get_atom_site_mixing_dict(
        atom_site_mixing_file_info, get_cif_300160_loop_values
    )

    # Mendeleev # - Ge 79, Rh 59, Sm 23
    assert len(atom_site_pair_dict) == 6
    assert atom_site_pair_dict[("Rh1", "Rh1")] == "4"
    assert atom_site_pair_dict[("Ge1", "Ge1")] == "4"
    assert atom_site_pair_dict[("Sm1", "Sm1")] == "4"
    assert atom_site_pair_dict[("Sm1", "Rh1")] == "4"
    assert atom_site_pair_dict[("Sm1", "Ge1")] == "4"
    assert atom_site_pair_dict[("Rh1", "Ge1")] == "4"


@pytest.mark.fast
def test_get_atom_site_mixing_dict_2(get_cif_527000_loop_values):
    """
    Pair: Rh2-Si 2.28 Å - deficiency_no_atomic_mixing
    Pair: Rh1-Rh1 2.524 Å - full_occupancy
    """
    atom_site_mixing_file_info = occupancy.get_atom_site_mixing_info(
        get_cif_527000_loop_values
    )

    atom_site_pair_dict = occupancy.get_atom_site_mixing_dict(
        atom_site_mixing_file_info, get_cif_527000_loop_values
    )

    # Mendeleev # - Rh 59, Si 78
    assert len(atom_site_pair_dict) == 6
    assert atom_site_pair_dict[("Rh1", "Si")] == "4"
    assert atom_site_pair_dict[("Rh1", "Rh1")] == "4"
    assert atom_site_pair_dict[("Rh1", "Rh2")] == "3"
    assert atom_site_pair_dict[("Rh2", "Rh2")] == "3"
    assert atom_site_pair_dict[("Si", "Si")] == "4"
    assert atom_site_pair_dict[("Rh2", "Si")] == "3"


@pytest.mark.fast
def test_get_atom_site_mixing_dict_3(get_cif_1831432_loop_values):
    """
    Mendeleev # - Fe 55, Ge 79
    1831432.cif
    Fe Fe 8 b 0.375 0.375 0.375 0.01
    Ge1 Ge 8 a 0.125 0.125 0.125 0.944
    Fe2 Fe 8 a 0.125 0.125 0.125 0.056

    Result:
    Fe-Fe 2.448 deficiency,
    Fe-Ge 2.448 mixing-deficiency,
    Fe-Fe 2.448 mixing-deficiency
    """

    atom_site_mixing_file_info = occupancy.get_atom_site_mixing_info(
        get_cif_1831432_loop_values
    )

    atom_site_pair_dict = occupancy.get_atom_site_mixing_dict(
        atom_site_mixing_file_info, get_cif_1831432_loop_values
    )

    assert len(atom_site_pair_dict) == 6
    assert atom_site_pair_dict[("Fe", "Fe")] == "3"
    assert atom_site_pair_dict[("Fe", "Fe2")] == "1"
    assert atom_site_pair_dict[("Fe", "Ge1")] == "1"
    assert atom_site_pair_dict[("Fe2", "Ge1")] == "2"
    assert atom_site_pair_dict[("Fe2", "Fe2")] == "2"
    assert atom_site_pair_dict[("Ge1", "Ge1")] == "2"


@pytest.mark.fast
def test_get_atom_site_mixing_dict_4(get_cif_529848_loop_values):
    """
    Mendeleev # - Ni 61, Sb 85
    529848.cif
    Ni1 Ni 4 a 0 0 0 0.92
    Sb2 Sb 4 a 0 0 0 0.08

    Result:
    529848: Ni-Sb 2.531 mixing
    """
    atom_site_mixing_file_info = occupancy.get_atom_site_mixing_info(
        get_cif_529848_loop_values
    )

    atom_site_pair_dict = occupancy.get_atom_site_mixing_dict(
        atom_site_mixing_file_info, get_cif_529848_loop_values
    )

    assert len(atom_site_pair_dict) == 3
    assert atom_site_pair_dict[("Ni1", "Ni1")] == "2"
    assert atom_site_pair_dict[("Sb2", "Sb2")] == "2"
    assert atom_site_pair_dict[("Ni1", "Sb2")] == "2"


@pytest.mark.fast
def test_get_atom_site_mixing_dict_5(get_cif_1617211_loop_values):
    """
    Mendeleev # - Fe 55, Si 78
    1617211.cif
    Si1 Si 2 h 0.5 0.5 0.2700 1
    Fe1A Fe 1 a 0 0 0 0.85008
    Si1B Si 1 a 0 0 0 0.06992

    Result:
    529848: Ni-Sb 2.531 mixing
    """
    atom_site_mixing_file_info = occupancy.get_atom_site_mixing_info(
        get_cif_1617211_loop_values
    )

    atom_site_pair_dict = occupancy.get_atom_site_mixing_dict(
        atom_site_mixing_file_info, get_cif_1617211_loop_values
    )

    assert len(atom_site_pair_dict) == 6
    assert atom_site_pair_dict[("Si1", "Si1")] == "4"
    assert atom_site_pair_dict[("Si1B", "Si1B")] == "1"
    assert atom_site_pair_dict[("Fe1A", "Fe1A")] == "1"
    assert atom_site_pair_dict[("Fe1A", "Si1")] == "1"
    assert atom_site_pair_dict[("Si1", "Si1B")] == "1"
    assert atom_site_pair_dict[("Fe1A", "Si1B")] == "1"
