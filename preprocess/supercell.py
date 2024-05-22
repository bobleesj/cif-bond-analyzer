import numpy as np
import gemmi
from preprocess import cif_parser
from util import prompt


def calculate_dist(point1, point2, cell_lengths, angles):
    """
    Calculates distance between two points using cell lengths and angles.
    """

    # Unpack points
    x1, y1, z1, label1 = point1
    x2, y2, z2, label2 = point2

    # Calculate differences in coordinates
    delta_x = x1 - x2
    delta_y = y1 - y2
    delta_z = z1 - z2

    # Calculate distances along each axis
    dx_sq = (cell_lengths[0] * delta_x) ** 2
    dy_sq = (cell_lengths[1] * delta_y) ** 2
    dz_sq = (cell_lengths[2] * delta_z) ** 2

    # Calculate cross terms
    cross_x = (
        2
        * cell_lengths[1]
        * cell_lengths[2]
        * np.cos(angles[0])
        * delta_y
        * delta_z
    )
    cross_y = (
        2
        * cell_lengths[2]
        * cell_lengths[0]
        * np.cos(angles[1])
        * delta_z
        * delta_x
    )
    cross_z = (
        2
        * cell_lengths[0]
        * cell_lengths[1]
        * np.cos(angles[2])
        * delta_x
        * delta_y
    )

    # Calculate squared distance
    result = dx_sq + dy_sq + dz_sq + cross_x + cross_y + cross_z

    # Calculate Euclidean distance
    distance = np.sqrt(result)

    return distance, label1, label2


def shift_and_append_points(
    points,
    atom_site_label,
    supercell_generation_method,
    is_flatten_points_only=False,
):
    """
    Shift and duplicate points to create supercell.
    """
    num_unit_cell_atom_count = len(points)
    translation_op_unit_cell_atom_num_threshold = 100
    # Method 1 - No sfhits
    # Method 2 - +1 +1 +1 shifts
    # Method 3 - +-1 +-1 +-1 shifts

    if (
        num_unit_cell_atom_count
        > translation_op_unit_cell_atom_num_threshold
        or is_flatten_points_only
    ):
        if supercell_generation_method == 1:
            shifts = np.array([[0, 0, 0]])
            shifted_points = points[:, None, :] + shifts[None, :, :]
            all_points = []
            for point_group in shifted_points:
                for point in point_group:
                    new_point = (*np.round(point, 5), atom_site_label)
                    all_points.append(new_point)
            return all_points

        if supercell_generation_method == 2:
            shifts = np.array(
                [
                    [0, 0, 0],
                    [1, 0, 0],
                    [0, 1, 0],
                    [0, 0, 1],
                    [1, 1, 0],
                    [1, 0, 1],
                    [0, 1, 1],
                    [1, 1, 1],
                ]
            )
            shifted_points = points[:, None, :] + shifts[None, :, :]
            all_points = []
            for point_group in shifted_points:
                for point in point_group:
                    new_point = (*np.round(point, 5), atom_site_label)
                    all_points.append(new_point)

            return all_points

        if supercell_generation_method == 3:
            shifts = np.array(
                [
                    [0, 0, 0],
                    [1, 0, 0],
                    [0, 1, 0],
                    [0, 0, 1],
                    [-1, 0, 0],
                    [0, -1, 0],
                    [0, 0, -1],
                    [1, 1, 0],
                    [1, -1, 0],
                    [-1, 1, 0],
                    [-1, -1, 0],
                    [1, 0, 1],
                    [1, 0, -1],
                    [0, 1, 1],
                    [0, 1, -1],
                    [-1, 0, 1],
                    [-1, 0, -1],
                    [0, -1, 1],
                    [0, -1, -1],
                    [1, 1, 1],
                    [1, 1, -1],
                    [1, -1, 1],
                    [1, -1, -1],
                    [-1, 1, 1],
                    [-1, 1, -1],
                    [-1, -1, 1],
                    [-1, -1, -1],
                ]
            )

            shifted_points = points[:, None, :] + shifts[None, :, :]
            all_points = []
            for point_group in shifted_points:
                for point in point_group:
                    new_point = (*np.round(point, 5), atom_site_label)
                    all_points.append(new_point)

            return all_points

    # General method for files below 100 atoms in the unit cell

    shifts = np.array(
        [
            # Existing shifts for -1, 0, 1
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [-1, 0, 0],
            [0, -1, 0],
            [0, 0, -1],
            [1, 1, 0],
            [1, -1, 0],
            [-1, 1, 0],
            [-1, -1, 0],
            [1, 0, 1],
            [1, 0, -1],
            [0, 1, 1],
            [0, 1, -1],
            [-1, 0, 1],
            [-1, 0, -1],
            [0, -1, 1],
            [0, -1, -1],
            [1, 1, 1],
            [1, 1, -1],
            [1, -1, 1],
            [1, -1, -1],
            [-1, 1, 1],
            [-1, 1, -1],
            [-1, -1, 1],
            [-1, -1, -1],
        ]
    )

    shifted_points = points[:, None, :] + shifts[None, :, :]
    all_points = []
    for point_group in shifted_points:
        for point in point_group:
            new_point = (*np.round(point, 5), atom_site_label)
            all_points.append(new_point)

    return all_points


def get_coords_list(block, loop_values):
    """
    Computes the new coordinates after applying
    symmetry operations to the initial coordinates.
    """

    loop_length = len(loop_values[0])
    coords_list = []
    for i in range(loop_length):
        atom_site_x = cif_parser.remove_string_braket(
            loop_values[4][i]
        )
        atom_site_y = cif_parser.remove_string_braket(
            loop_values[5][i]
        )
        atom_site_z = cif_parser.remove_string_braket(
            loop_values[6][i]
        )
        atom_site_label = loop_values[0][i]

        coords_after_symmetry_operations = (
            get_coords_after_sym_operations(
                block,
                float(atom_site_x),
                float(atom_site_y),
                float(atom_site_z),
                atom_site_label,
            )
        )
        coords_list.append(coords_after_symmetry_operations)

    return coords_list


def get_coords_after_sym_operations(
    block,
    atom_site_fract_x,
    atom_site_fract_y,
    atom_site_fract_z,
    atom_site_label,
):
    """
    Generates a list of coordinates for each atom site
    """
    all_coords = set()
    for operation in block.find_loop(
        "_space_group_symop_operation_xyz"
    ):
        operation = operation.replace("'", "")
        try:
            op = gemmi.Op(operation)
            new_x, new_y, new_z = op.apply_to_xyz(
                [
                    atom_site_fract_x,
                    atom_site_fract_y,
                    atom_site_fract_z,
                ]
            )
            new_x = round(new_x, 5)
            new_y = round(new_y, 5)
            new_z = round(new_z, 5)

            all_coords.add((new_x, new_y, new_z, atom_site_label))

        except RuntimeError as e:
            print(f"Skipping operation '{operation}': {str(e)}")
            raise RuntimeError(
                "An error occurred while processing symmetry operation"
            ) from e

    return list(all_coords)


def flatten_original_coordinates(all_coords):
    points = np.array(
        [list(map(float, coord[:-1])) for coord in all_coords]
    )
    return points


def get_points_and_labels(
    all_coords_list,
    loop_values,
    supercell_generation_method=3,
    is_flatten_points_only=False,
):
    """
    Process coordinates and loop values to extract points, labels, and atom types.
    """
    all_points = []
    unique_labels = []
    unique_atoms_tuple = []

    # Get the total number of atoms in the unit cell

    for i, all_coords in enumerate(all_coords_list):
        points = flatten_original_coordinates(all_coords)
        atom_site_label = loop_values[0][i]
        atom_site_type = loop_values[1][i]

        unique_labels.append(atom_site_label)
        unique_atoms_tuple.append(atom_site_type)
        all_points.extend(
            shift_and_append_points(
                points,
                atom_site_label,
                supercell_generation_method,
                is_flatten_points_only,
            )
        )

        if atom_site_type in atom_site_label:
            continue

        if (
            cif_parser.get_atom_type(atom_site_label)
            != atom_site_type
        ):
            raise RuntimeError(
                "Different elements found in atom site and label"
            )

    return list(set(all_points)), unique_labels, unique_atoms_tuple


def distance_to_origin(point):
    """
    Calculate the Euclidean distance from a given
    point to the origin in 3D space.
    """

    x, y, z, _ = point
    return (x**2 + y**2 + z**2) ** 0.5


def calc_dist_two_cart_points(point1, point2):
    """
    Calculate the Euclidean distance between two points
    in Cartesian coordinates.
    """
    point1 = np.array(point1)
    point2 = np.array(point2)
    diff = point2 - point1
    distance = np.linalg.norm(diff)

    return distance


def fractional_to_cartesian(
    fractional_coords, cell_lengths, rad_angles
):
    """
    Converts fractional coordinates to Cartesian
    coordinates using cell lengths and angles.
    """
    alpha, beta, gamma = rad_angles

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
            [
                0,
                b * sin_gamma,
                c * (cos_alpha - cos_beta * cos_gamma) / sin_gamma,
            ],
            [0, 0, volume / (a * b * sin_gamma)],
        ]
    )

    # Convert fractional coordinates to Cartesian coordinates
    fractional_coords = np.array(fractional_coords)
    if fractional_coords.ndim == 1:
        fractional_coords = fractional_coords[
            :, np.newaxis
        ]  # Convert to column vector if necessary

    cartesian_coords = np.dot(matrix, fractional_coords).flatten()

    return cartesian_coords
