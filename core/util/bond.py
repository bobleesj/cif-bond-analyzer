def get_ordered_bond_labels_from_RMX(
    R_element, M_element, X_element
) -> list[str]:
    return [
        f"{R_element}-{R_element}",  # Self-pair for R
        f"{R_element}-{M_element}",  # R-M pair
        f"{M_element}-{M_element}",  # Self-pair for M
        f"{M_element}-{X_element}",  # M-X pair
        f"{X_element}-{X_element}",  # Self-pair for X
        f"{R_element}-{X_element}",  # R-X pair
    ]


def get_ordered_bond_labels_from_AB(A_element, B_element) -> list[str]:
    return [
        f"{A_element}-{A_element}",
        f"{A_element}-{B_element}",
        f"{B_element}-{B_element}",
    ]
