import pandas as pd
import numpy as np
from cifkit.utils import string_parser


def compute_delta(ref_label: str, other_label: str, dist: float) -> float:
    """
    Calculate the percentage difference between a provided distance
    and the sum of atomic radii.
    """

    ref_element = string_parser.get_atom_type_from_label(ref_label)
    ref_element_rad = get_element_radius(ref_element)

    other_element = string_parser.get_atom_type_from_label(other_label)
    other_element_rad = get_element_radius(other_element)

    rad_sum = ref_element_rad + other_element_rad
    delta_percent = np.round(
        (float(dist) - rad_sum) * 100 / rad_sum,
        3,
    )
    return delta_percent


def get_element_radius(
    ref_element: float, filename="radii.xlsx", sheet_name="data"
) -> float:
    """
    Retrieve the atomic radius for a specified element from an Excel file.
    """
    # Read the Excel file into a DataFrame
    df = pd.read_excel(filename, sheet_name=sheet_name)

    # Filter the DataFrame to get the radius for the reference element
    ref_element_rad = df.loc[df["Element"] == ref_element, "Radius"].values[0]

    return ref_element_rad
