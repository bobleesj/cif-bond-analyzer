import numpy as np


def get_radians_from_degrees(angles):
    """
    Converts angles from degrees to radians and round to 5 decimal places.
    """
    radians = [round(np.radians(angle), 5) for angle in angles]

    return radians


def rounded_distance(distance, precision=2):
    """
    Round a distance value to a specified precision.
    """
    
    return round(distance, precision)


