def remove_string_braket(value_string):
    """
    Removes parentheses from a value string and convert to float if possible.
    """
    return (
        float(value_string.split("(")[0])
        if "(" in value_string
        else float(value_string)
    )


def parse_formulas_with_underscore(formula_set):
    # Filter formulas containing an underscore
    filtered_formulas = [
        formula for formula in formula_set if "_" in formula
    ]

    # Parse the filtered formulas to separate the base formula and the suffix
    parsed_formulas = []
    for formula in filtered_formulas:
        base, suffix = formula.split(
            "_", 1
        )  # Split on the first underscore only
        parsed_formulas.append((base, suffix))

    return parsed_formulas
