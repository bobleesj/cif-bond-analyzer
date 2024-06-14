import numpy as np
from preprocess.cif_parser import get_atom_type
from util import formula_parser
from itertools import combinations


def get_bond_counts(formula: str, connections: dict[str, list]) -> dict:
    """
    Return a dictionary containing bond pairs and counts per label site.
    """

    all_bond_pairs = get_all_bond_pairs(formula)

    # Initialize the dictionary to hold bond pair counts for each label
    bond_pair_data: dict = {}

    for label, label_connections in connections.items():
        # Initialize the bond count for the current label
        bond_pair_data[label] = {}

        # Get the atom type for the reference label
        ref_element = get_atom_type(label)

        # Iterate over each connection for the current label
        for conn in label_connections:
            (
                conn_label,
                _,
                _,
                _,
            ) = conn

            # Get the atom type for the connected label
            conn_element = get_atom_type(conn_label)

            # Create a tuple representing the bond pair, sorted
            sorted_bond_pair = tuple(sorted((ref_element, conn_element)))

            # Check if the bond pair is one of the valid pairs
            if sorted_bond_pair in all_bond_pairs:
                if sorted_bond_pair in bond_pair_data[label]:
                    bond_pair_data[label][sorted_bond_pair] += 1
                else:
                    bond_pair_data[label][sorted_bond_pair] = 1

    return bond_pair_data


def get_bond_fraction(bond_pair_data: dict) -> dict[tuple[str, str], float]:
    """
    Calculate the fraction of each bond type across all labels.
    """
    total_bond_counts: dict[tuple[str, str], float] = {}
    total_bonds = 0

    # Sum up bond counts for each bond type
    for bonds in bond_pair_data.values():
        for bond_type, count in bonds.items():
            if bond_type in total_bond_counts:
                total_bond_counts[bond_type] += count
            else:
                total_bond_counts[bond_type] = count
            total_bonds += count

    # Calculate fractions
    bond_fractions = {
        bond_type: round(count / total_bonds, 3)
        for bond_type, count in total_bond_counts.items()
    }

    return bond_fractions


def get_heterogenous_element_pairs(
    formula_str: str,
) -> set[tuple[str, str]]:
    """
    Generate all possible unique alphabetically sorted heterogenious pairs.
    """
    elements = formula_parser.get_unique_elements(formula_str)

    # Generate all possible pairs using combinations ensuring uniqueness
    all_pairs = set(combinations(sorted(elements), 2))

    # 'combinations' already sorts them alphabetically, see the test
    return all_pairs


def get_homogenous_element_pairs(
    formula_str: str,
) -> set[tuple[str, str]]:
    """
    Generate all possible sorted homogenous bonding pairs from a formula.
    """
    elements = formula_parser.get_unique_elements(formula_str)
    # Sort the elements alphabetically
    elements.sort()
    homogenous_pairs = [(element, element) for element in elements]
    return set(homogenous_pairs)


def get_all_bond_pairs(formula_str: str) -> set[tuple[str, str]]:
    heterogeneous_bond_pairs = get_heterogenous_element_pairs(formula_str)
    homogenous_bond_pairs = get_homogenous_element_pairs(formula_str)
    return heterogeneous_bond_pairs.union(homogenous_bond_pairs)
