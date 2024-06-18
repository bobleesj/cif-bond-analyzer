import pytest
import postprocess.pair_order as pair_order


@pytest.mark.fast
def test_sort_label_tuple():
    label_pair_tuple = ("Fe1B", "Fe1A")
    sorted_label_pair_tuple = pair_order.sort_label_tuple(
        label_pair_tuple
    )
    assert sorted_label_pair_tuple == ("Fe1A", "Fe1B")

    label_pair_tuple = ("Co2B", "Co2A")
    sorted_label_pair_tuple = pair_order.sort_label_tuple(
        label_pair_tuple
    )
    assert sorted_label_pair_tuple == ("Co2A", "Co2B")


@pytest.mark.fast
def test_order_pair_by_mendeleev_and_label():
    # U = 20    Rh = 59    In = 75
    expected = pair_order.order_pair_by_mendeleev(
        ("In", "U")
    )
    assert expected == ("U", "In")

    expected = pair_order.order_pair_by_mendeleev(
        ("U", "In")
    )
    assert expected == ("U", "In")

    expected = pair_order.order_pair_by_mendeleev(
        ("Rh", "U")
    )
    assert expected == ("U", "Rh")

    expected = pair_order.order_pair_by_mendeleev(
        ("In", "Rh")
    )
    assert expected == ("Rh", "In")

    expected = pair_order.order_pair_by_mendeleev(
        ("Rh4", "Rh2")
    )
    assert expected == ("Rh2", "Rh4")

    expected = pair_order.order_pair_by_mendeleev(
        ("Co2B", "Co2A")
    )
    assert expected == ("Co2A", "Co2B")

    expected = pair_order.order_pair_by_mendeleev(
        ("Co2A", "Co2B")
    )
    assert expected == ("Co2A", "Co2B")


@pytest.mark.fast
def test_sort_tuple_in_list():
    tuple_pairs = [("Fe1B", "Fe1A"), ("Si1B", "Si1")]
    sorted_tuple_pairs = pair_order.sort_tuple_in_list(
        tuple_pairs
    )
    assert sorted_tuple_pairs == [
        ("Fe1A", "Fe1B"),
        ("Si1", "Si1B"),
    ]

    tuple_pairs = [("Rh2", "Rh1"), ("Si1C", "Si1A")]
    sorted_tuple_pairs = pair_order.sort_tuple_in_list(
        tuple_pairs
    )
    assert sorted_tuple_pairs == [
        ("Rh1", "Rh2"),
        ("Si1A", "Si1C"),
    ]

    tuple_pairs = [("Co2A", "Co1A")]
    sorted_tuple_pairs = pair_order.sort_tuple_in_list(
        tuple_pairs
    )
    assert sorted_tuple_pairs == [("Co1A", "Co2A")]
