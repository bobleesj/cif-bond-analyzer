"""Provides functions for sorting tuples of atomic labels by Mendeleev
numbers."""

import pandas as pd
from cifkit.utils.cif_parser import get_atom_type_from_label


def get_mendeleev_num_from_tuple(pair_tuple):
    """Parse Mendeleev number for each label in the tuple."""
    # Parse the first and second elements
    first_element = get_atom_type_from_label(pair_tuple[0])
    second_element = get_atom_type_from_label(pair_tuple[1])

    # Read Excel
    df = pd.read_excel("data/element_Mendeleev_numbers.xlsx")

    # Get Mendeleev number for the first element
    first_mendeleev_num = df.loc[
        df["Symbol"] == first_element, "Mendeleev number"
    ].iloc[0]

    # Get Mendeleev number for the second element
    second_mendeleev_num = df.loc[
        df["Symbol"] == second_element, "Mendeleev number"
    ].iloc[0]

    return first_mendeleev_num, second_mendeleev_num


def order_pair_by_mendeleev(label_pair_tuple):
    """Order atomic label tuples based on Mendeleev numbers."""
    first_label = label_pair_tuple[0]
    second_label = label_pair_tuple[1]

    (
        first_mendeleev_num,
        second_mendeleev_num,
    ) = get_mendeleev_num_from_tuple(label_pair_tuple)

    # First element num must be smaller
    if first_mendeleev_num > second_mendeleev_num:
        return (second_label, first_label)

    # If first and second have the same mendeleev num, sort
    elif first_mendeleev_num == second_mendeleev_num:
        return sort_label_tuple(label_pair_tuple)

    # If it in correct order, return as it is
    else:
        return label_pair_tuple


def sort_label_tuple(label_tuple):
    """Sort a tuple of labels."""
    return tuple(sorted(label_tuple))


def sort_tuple_in_list(tuple_list):
    """Sort a list of tuples containing labels."""
    return [tuple(sorted(item)) for item in tuple_list]


def sort_tuple_by_mendeleevin_list(tuple_list):
    """Sort a list of tuples containing labels."""
    return [tuple(order_pair_by_mendeleev(item)) for item in tuple_list]
