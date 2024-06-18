from util import data, formula_parser


def sort_by_mendeleev(formula):
    mendeleev_numbers = data.get_mendeleev_numbers(
        "data/element_Mendeleev_numbers.xlsx"
    )

    sorted_formula = sorted(
        formula,
        key=lambda x: mendeleev_numbers.get(
            x, float("inf")
        ),
    )

    return list(sorted_formula)
