from itertools import product

from cifkit.utils.bond_pair import order_tuple_pair_by_mendeleev


def get_sorted_missing_pairs(global_element_pair_dict):
    """Return label tuple list containing pairs not found from CIF."""

    all_pairs = get_all_ordered_pairs_from_set(global_element_pair_dict)

    pairs_found = set(
        tuple(order_tuple_pair_by_mendeleev(tuple(pair.split("-"))))
        for pair in global_element_pair_dict.keys()
    )

    # Sort the pairs in the data as well before comparison
    missing_label_pairs = [
        pair for pair in all_pairs if pair not in pairs_found
    ]

    return missing_label_pairs


def get_all_ordered_pairs_from_set(pair_dict):
    """Generates all possible unique ordered label pairs."""
    unique_labels = set()

    for pair in pair_dict.keys():
        element_1, element_2 = pair.split("-")
        unique_labels.add(element_1)
        unique_labels.add(element_2)

    # Generate all possible pairs (with ordering matter)
    all_pairs = list(product(unique_labels, repeat=2))

    # Order pairs based on Mendeleev ordering
    all_pairs_ordered = [
        tuple(order_tuple_pair_by_mendeleev(pair)) for pair in all_pairs
    ]

    # Remove duplicates from all possible pairs
    all_pairs_ordered_unique = list(set(all_pairs_ordered))

    return all_pairs_ordered_unique


def get_all_ordered_pairs_from_list(pair_list):
    """Generates all possible unique ordered pairs following a specific
    order."""
    unique_labels = sorted(
        set(element for pair in pair_list for element in pair.split("-"))
    )

    # Generate all possible pairs (with ordering matter)
    all_pairs = list(product(unique_labels, repeat=2))

    # Order pairs based on Mendeleev ordering and remove duplicates
    # Sort the list of unique ordered pairs based on the first element index
    all_pairs_ordered = sorted(
        set(tuple(order_tuple_pair_by_mendeleev(pair)) for pair in all_pairs),
        key=lambda x: (
            unique_labels.index(x[0]),
            unique_labels.index(x[1]),
        ),
    )

    return all_pairs_ordered
