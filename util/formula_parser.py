import re


def get_normalized_formula(formula):
    demical_places = 3
    index_sum = 0
    normalized_formula_parts = []
    parsed_formula_set = get_parsed_formula(formula)

    # Calculate the sum of all indices
    for element, element_index in parsed_formula_set:
        if element_index == "":
            index_sum += 1  # Treat missing indices as 1
        else:
            index_sum += float(element_index)

    for element, element_index in parsed_formula_set:
        if element_index == "":
            normalized_index = 1 / index_sum
        else:
            normalized_index = float(element_index) / index_sum

        normalized_formula_parts.append(
            f"{element}{normalized_index:.{demical_places}f}"
        )

    # Join all parts into one string for the normalized formula
    normalized_formula_str = "".join(normalized_formula_parts)
    return normalized_formula_str


def get_num_element(formula):
    elements = get_parsed_formula(formula)
    return


def get_parsed_formula(formula):
    pattern = r"([A-Z][a-z]*)(\d*\.?\d*)"
    elements = re.findall(pattern, formula)
    return elements


def get_parsed_norm_formula(formula):
    normalized_formula = get_normalized_formula(formula)
    parsed_normalized_formula = get_parsed_formula(normalized_formula)
    return parsed_normalized_formula


def get_unique_elements_from_formulas(formulas):
    unique_elements = set()  # Create a set to store unique elements

    for formula in formulas:
        parsed_formula = get_parsed_formula(
            formula
        )  # Assume this function returns a list of tuples
        for element, _ in parsed_formula:
            if element:  # Ensure that element is not empty
                unique_elements.add(
                    element
                )  # Add the element to the set

    return unique_elements


def get_subscripted_formula(formula):
    # Use regular expression to find elements and numbers
    formatted_formula = re.sub(
        r"([A-Z][a-z]*)(\d*\.?\d*)", r"\1$_{\2}$", formula
    )
    return formatted_formula
