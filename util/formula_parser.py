import re
from util import sort


def get_normalized_formula(formula):
    """
    Returns a formula wlth the stoichiometry coefficient sum of 1
    """
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


def get_unique_elements(formula: str) -> list[str]:
    "Return a set of elements parsed from a formula."
    elements = get_parsed_formula(formula)
    unique_elements = [element for element, _ in elements]
    return unique_elements


def get_num_element(formula):
    """
    Returns the number of elements.
    """
    elements = get_parsed_formula(formula)
    return len(elements)


def get_parsed_formula(formula):
    """
    Returns a list of tuples, each tuple containing element and index.
    """

    pattern = r"([A-Z][a-z]*)(\d*\.?\d*)"
    elements = re.findall(pattern, formula)
    return elements


def get_parsed_norm_formula(formula):
    """
    Returns a list of tuples, each tuple containing element
    and normalized index.
    """
    normalized_formula = get_normalized_formula(formula)
    parsed_normalized_formula = get_parsed_formula(normalized_formula)
    return parsed_normalized_formula


def get_unique_elements_from_formulas(formulas: list[str]):
    """
    Returns unique elements from a list of formulas.
    """
    unique_elements = set()  # Create a set to store unique elements

    for formula in formulas:
        parsed_formula = get_parsed_formula(
            formula
        )  # Assume this function returns a list of tuples
        for element, _ in parsed_formula:
            if element:  # Ensure that element is not empty
                unique_elements.add(element)  # Add the element to the set

    return unique_elements


def get_subscripted_formula(formula):
    """
    Returns a subscripted formula used for plotting.
    """
    # Use regular expression to find elements and numbers
    formatted_formula = re.sub(
        r"([A-Z][a-z]*)(\d*\.?\d*)", r"\1$_{\2}$", formula
    )
    return formatted_formula


def get_mendeleev_sorted_formula(formula: str) -> list:
    unique_elements = set()
    parsed_formula = get_parsed_formula(formula)
    for element, _ in parsed_formula:
        unique_elements.add(element)
    sorted_unique_elements = sort.sort_by_mendeleev(unique_elements)
    return sorted_unique_elements


def get_RMX_sorted_formula_from_formulas(unique_formulas):
    """
    Processe a set of chemical formulas, sorts the unique elements by
    Mendeleev numbers, and returns the sorted elements as R, M, and X.
    """
    # Parse unique elements from the given set of formulas
    unique_elements = get_unique_elements_from_formulas(unique_formulas)

    # Sort these elements by their Mendeleev numbers
    sorted_unique_elements = sort.sort_by_mendeleev(unique_elements)

    # Ensure that there are at least three elements to unpack
    if len(sorted_unique_elements) < 3:
        raise ValueError("Not enough elements to form R, M, X.")

    # Unpack the first three elements as R, M, X
    R_element, M_element, X_element = sorted_unique_elements[:3]

    return R_element, M_element, X_element


def generate_ordered_bond_labels_from_RMX(
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


def count_formula_with_tags_in_ternary(formula_tag_tuples, R, M, X):
    """
    Count RM_ht, RM_lt, RX_ht, RX_lt, MX_lt, MX_ht combinations,
    and other combinations with unspecified suffixes,
    given the definitions of R, M, and X elements.
    """
    counts = {
        "RM_ht": 0,
        "RM_lt": 0,
        "RX_ht": 0,
        "RX_lt": 0,
        "MX_lt": 0,
        "MX_ht": 0,
        "RM_others": 0,
        "RX_others": 0,
        "MX_others": 0,
    }

    # Define a helper to extract elements from formula
    def extract_elements(formula):
        return re.findall(r"[A-Z][a-z]*", formula)

    # Process each formula and suffix
    for formula, suffix in formula_tag_tuples:
        elements = extract_elements(formula)
        elements_set = set(elements)

        # Check and increment the appropriate counter
        if elements_set == {R, M}:
            if suffix == "ht":
                counts["RM_ht"] += 1
            elif suffix == "lt":
                counts["RM_lt"] += 1
            else:
                counts["RM_others"] += 1
        if elements_set == {R, X}:
            if suffix == "ht":
                counts["RX_ht"] += 1
            elif suffix == "lt":
                counts["RX_lt"] += 1
            else:
                counts["RX_others"] += 1
        if elements_set == {M, X}:
            if suffix == "ht":
                counts["MX_ht"] += 1
            elif suffix == "lt":
                counts["MX_lt"] += 1
            else:
                counts["MX_others"] += 1

    return counts


def extract_tag(formula_tag):
    # Split the string by underscore and return the last element
    parts = formula_tag.split("_")
    if len(parts) > 1:
        # Check if the last part is 'rt' and return None if it is
        if parts[-1] == "rt":
            return None
        return parts[-1]  # Return the tag part
    return None  # Return None if there is no tag


def get_composition_from_binary_ternary(
    formula: str, elements: tuple[str]
) -> tuple[float]:
    # Regex to find elements followed by optional stoichiometric numbers (including decimals)
    pattern = r"(" + "|".join(elements) + r")(\d*\.?\d*)"
    matches = re.findall(pattern, formula)
    parts_dict = {
        el: 0 for el in elements
    }  # Initialize each element's count as 0

    for element, count in matches:
        if count == "":
            parts_dict[
                element
            ] = 1  # Default to 1 if no number is given after an element
        else:
            parts_dict[element] = float(
                count
            )  # Use float to accommodate decimal values

    total = sum(parts_dict.values())
    if total > 0:
        normalized_parts = [
            round(parts_dict[el] / total, 3) for el in elements
        ]  # Normalize and round to 3 decimal places
    else:
        normalized_parts = [0] * len(
            elements
        )  # If total is 0, return a list of zeros

    return (normalized_parts[0], normalized_parts[1], normalized_parts[2])
