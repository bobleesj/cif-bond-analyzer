import pytest
import postprocess.pair_order as pair_order


@pytest.mark.fast
def test_order_pair_based_on_mendeleev_num():

    # U = 20    Rh = 59    In = 75
    expected_tuple = pair_order.order_pair_based_on_mendeleev_num(("In", "U"))
    assert expected_tuple == ("U", "In")

    expected_tuple = pair_order.order_pair_based_on_mendeleev_num(("U", "In"))
    assert expected_tuple == ("U", "In")

    expected_tuple = pair_order.order_pair_based_on_mendeleev_num(("Rh", "U"))
    assert expected_tuple == ("U", "Rh")

    expected_tuple = pair_order.order_pair_based_on_mendeleev_num(("In", "Rh"))
    assert expected_tuple == ("Rh", "In")


@pytest.mark.fast
def test_cheeck_is_pair_ordered_based_on_mendeleev_num():
    # U = 20    Rh = 59    In = 75

    is_ordered = pair_order.is_pair_ordered_by_mendeleev(("In", "In"))
    assert is_ordered is True

    is_ordered = pair_order.is_pair_ordered_by_mendeleev(("In", "U"))
    assert is_ordered is not True

    is_ordered = pair_order.is_pair_ordered_by_mendeleev(("U", "In"))
    assert is_ordered is True

    is_ordered = pair_order.is_pair_ordered_by_mendeleev(("Rh", "U"))
    assert is_ordered is not True

    is_ordered = pair_order.is_pair_ordered_by_mendeleev(("In", "Rh"))
    assert is_ordered is not True


@pytest.mark.now
def test_sort_tuple_in_list():
    tuple_pairs = [("Fe1B", "Fe1A"), ("Si1B", "Si1")]
    sorted_tuple_pairs = pair_order.sort_tuple_in_list(tuple_pairs)
    assert sorted_tuple_pairs == [("Fe1A", "Fe1B"), ("Si1", "Si1B")]

    tuple_pairs = [("Rh2", "Rh1"), ("Si1C", "Si1A")]
    sorted_tuple_pairs = pair_order.sort_tuple_in_list(tuple_pairs)
    assert sorted_tuple_pairs == [("Rh1", "Rh2"), ("Si1A", "Si1C")]

    sorted_tuple_pairs = pair_order.sort_tuple_in_list(tuple_pairs)
    assert sorted_tuple_pairs == [("Rh1", "Rh2"), ("Si1A", "Si1C")]
