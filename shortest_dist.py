import json
import numpy as np
from click import echo
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from preprocess import cif_parser, cif_parser_handler
from preprocess import supercell
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# Function to calculate the Euclidean distance to the origin
def distance_to_origin(point):
    x, y, z, _ = point
    return (x**2 + y**2 + z**2) ** 0.5


def calc_dist_two_cart_points(point1, point2):
    point1 = np.array(point1)
    point2 = np.array(point2)
    diff = point2 - point1
    distance = np.linalg.norm(diff)

    return distance


def fractional_to_cartesian(fractional_coords, cell_lengths, rad_angles):
    """
    Converts fractional coordinates to Cartesian coordinates using cell lengths and angles.
    """
    alpha, beta, gamma = rad_angles  # Assuming these angles are already in radians

    # Calculate the components of the transformation matrix
    a, b, c = cell_lengths
    cos_alpha = np.cos(alpha)
    cos_beta = np.cos(beta)
    cos_gamma = np.cos(gamma)
    sin_gamma = np.sin(gamma)

    # The volume of the unit cell
    volume = (
        a
        * b
        * c
        * np.sqrt(
            1
            - cos_alpha**2
            - cos_beta**2
            - cos_gamma**2
            + 2 * cos_alpha * cos_beta * cos_gamma
        )
    )

    # Transformation matrix from fractional to Cartesian coordinates
    matrix = np.array(
        [
            [a, b * cos_gamma, c * cos_beta],
            [0, b * sin_gamma, c * (cos_alpha - cos_beta * cos_gamma) / sin_gamma],
            [0, 0, volume / (a * b * sin_gamma)],
        ]
    )

    # Convert fractional coordinates to Cartesian coordinates
    # Ensure fractional_coords is a column vector for matrix multiplication
    fractional_coords = np.array(fractional_coords)
    if fractional_coords.ndim == 1:
        fractional_coords = fractional_coords[
            :, np.newaxis
        ]  # Convert to column vector if necessary

    cartesian_coords = np.dot(matrix, fractional_coords).flatten()

    return cartesian_coords


def get_cutoff_dist_info():
    # Select the CIF file - Example with "RhSb2.cif"
    file_path = "RhSb2.cif"
    cutoff_radius = 4.0  # Define the cutoff radius in Ångströms
    result = cif_parser_handler.get_cif_info(file_path, cif_parser.get_loop_tags())
    _, lengths, angles_rad, _, all_points, unique_labels, _ = result

    # Initialize the dictionary to hold cutoff distance information
    cutoff_dist_info = {}

    # Loop over unique labels to find the closest points and their distances
    for label in unique_labels:
        cutoff_dist_info[label] = []
        point1 = next((point for point in all_points if point[3] == label), None)

        if not point1:
            continue

        fractional_coord_1 = [point1[0], point1[1], point1[2]]
        cart_coords_point_1 = fractional_to_cartesian(fractional_coord_1, lengths, angles_rad)

        for point2 in all_points:
            if point1[:3] == point2[:3]:
                continue

            frac_coord_2 = [point2[0], point2[1], point2[2]]
            cart_coords_point_2 = fractional_to_cartesian(frac_coord_2, lengths, angles_rad)

            dist = calc_dist_two_cart_points(cart_coords_point_1, cart_coords_point_2)
            if dist <= cutoff_radius:
                cutoff_dist_info[label].append({
                    "label": point2[3],
                    "point1_coord": cart_coords_point_1.tolist(),
                    "point2_coord": cart_coords_point_2.tolist(),
                    "distance": dist
                })

    # Write the information to a JSON file
    with open(f'shortest_dist_{cutoff_radius}.json', 'w') as outfile:
        json.dump(cutoff_dist_info, outfile, indent=4)

# Call the function to execute
get_cutoff_dist_info()


if __name__ == "__main__":
    get_cutoff_dist_info()
