def get_ordered_bond_labels_from_RMX(R: str, M: str, X: str) -> list[str]:
    """Generates a list of bond labels for a ternary compound based on
    the elements provided."""

    return [
        f"{R}-{R}",
        f"{R}-{M}",
        f"{M}-{M}",
        f"{M}-{X}",
        f"{X}-{X}",
        f"{R}-{X}",
    ]


def get_ordered_bond_labels_from_AB(A: str, B: str) -> list[str]:
    """Generates a list of bond labels for a binary compound based on
    the elements provided."""
    return [
        f"{A}-{A}",
        f"{A}-{B}",
        f"{B}-{B}",
    ]
