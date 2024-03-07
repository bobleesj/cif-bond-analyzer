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
