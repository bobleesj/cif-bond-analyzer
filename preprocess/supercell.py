import numpy as np
from preprocess.cif_parser import *

def calculate_distance(point1, point2, cell_lengths, angles):
    """
    Calculates the Euclidean distance between two points using the given cell lengths and angles.
    """
    delta_x1, delta_y1, delta_z1, label1 = list(map(float, point1[:-1])) + [point1[-1]]
    delta_x2, delta_y2, delta_z2, label2 = list(map(float, point2[:-1])) + [point2[-1]]

    result = (
        (cell_lengths[0] * (delta_x1 - delta_x2))**2 +
        (cell_lengths[1] * (delta_y1 - delta_y2))**2 +
        (cell_lengths[2] * (delta_z1 - delta_z2))**2 +
        2 * cell_lengths[1] * cell_lengths[2] * np.cos(angles[0]) * (delta_y1 - delta_y2) * (delta_z1 - delta_z2) +
        2 * cell_lengths[2] * cell_lengths[0] * np.cos(angles[1]) * (delta_z1 - delta_z2) * (delta_x1 - delta_x2) +
        2 * cell_lengths[0] * cell_lengths[1] * np.cos(angles[2]) * (delta_x1 - delta_x2) * (delta_y1 - delta_y2)
    )

    distance = np.sqrt(result)

    return distance, label1, label2


def shift_and_append_points(points, atom_site_label):
    """
    Shift and duplicate points to create a 2 by 2 by 2 supercell.
    """
    shifts = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1],
                        [-1, 0, 0], [0, -1, 0], [-1, -1, 0], [0, 0, -1], [1, 0, -1], [0, -1, -1], [-1, -1, -1]])
    shifted_points = points[:, None, :] + shifts[None, :, :]
    all_points = []
    for point_group in shifted_points:
        for point in point_group:
            new_point = (*np.round(point,5), atom_site_label)
            all_points.append(new_point)

    return all_points


def get_coords_list(block, loop_values):
    """
    Computes the new coordinates after applying symmetry operations to the initial coordinates.
    """
    
    loop_length = len(loop_values[0])
    coords_list = []
    for i in range(loop_length):
        atom_site_x, atom_site_y, atom_site_z = remove_string_braket(loop_values[4][i]), remove_string_braket(loop_values[5][i]), remove_string_braket(loop_values[6][i])
        atom_site_label = loop_values[0][i]
        atom_type_symbol = loop_values[1][i]

        # print(atom_site_x, atom_site_y, atom_site_z, atom_site_label, atom_type_symbol)
        coordinates_after_symmetry_operations = get_coords_after_sym_operations(block, float(atom_site_x), float(atom_site_y), float(atom_site_z), atom_site_label)
        coords_list.append(coordinates_after_symmetry_operations)

    return coords_list


def get_coords_after_sym_operations(block, atom_site_fract_x, atom_site_fract_y, atom_site_fract_z, atom_site_label):
    """
    Generates a list of coordinates for each atom site in the block.
    """
    all_coords = set()
    for operation in block.find_loop("_space_group_symop_operation_xyz"):
        operation = operation.replace("'", "")
        try:
            op = gemmi.Op(operation)
            new_x, new_y, new_z = op.apply_to_xyz([atom_site_fract_x, atom_site_fract_y, atom_site_fract_z])
            new_x = round(new_x, 5)
            new_y = round(new_y, 5)
            new_z = round(new_z, 5)

            all_coords.add((new_x, new_y, new_z, atom_site_label))

        except RuntimeError as e:
            print(f"Skipping operation '{operation}': {str(e)}")
            raise RuntimeError("An error occurred while processing symmetry operation") from e

    return list(all_coords)


def get_points_and_labels(all_coords_list, loop_values):
    """
    Process coordinates and loop values to extract points, labels, and atom types.
    """
    all_points = []
    unique_labels = []
    unique_atoms_tuple = []
    for i, all_coords in enumerate(all_coords_list):
        points = np.array([list(map(float, coord[:-1])) for coord in all_coords])
        atom_site_label = loop_values[0][i]
        atom_site_type = loop_values[1][i]
        
        unique_labels.append(atom_site_label)
        unique_atoms_tuple.append(atom_site_type)
        all_points.extend(shift_and_append_points(points, atom_site_label))

        '''
        20240221 - switch to containing the label for the case of
        Co,Ni1 Co 4 a 0 0 0 0.50
        '''

        if atom_site_type in atom_site_label:
            continue
        elif get_atom_type(atom_site_label) != atom_site_type:
            raise RuntimeError("Different elements found in atom site and label")

    return list(set(all_points)), unique_labels, unique_atoms_tuple


def get_atomic_pair_list(flattened_points, cell_lengths, angles):
    """
    Calculate atomic distances and properties between pairs of points.
    """
    
    atomic_info_list = []
    pairs_set = set()

    # i, and j refers to nth atom in the 2x2x2 supercell
    # If there are 3,000 atoms total, ith atoms loops through every jth atom
    # no distance between the same atom
    for i, point1 in enumerate(flattened_points):
        distances_from_point_i = []

        for j, point2 in enumerate(flattened_points):
            if i != j:
                pair = tuple(sorted([i, j]))  # Sort the pair so (i, j) is treated as equivalent to (j, i)
                if pair not in pairs_set:  # Check if we've already processed this pair
                    distance, atom_label1, atom_label2 = calculate_distance(point1, point2, cell_lengths, angles)
                    if abs(distance) > 1e-8:  # Update the condition with the tolerance value
                        distances_from_point_i.append({
                            'point_pair': (i + 1, j + 1),
                            'labels': (atom_label1, atom_label2),
                            'coordinates': (point1[:3], point2[:3]),  # include coordinates
                            'distance': np.round(distance, 5)
                        })
                        pairs_set.add(pair)  # Add the pair to the set of seen pairs

        distances_from_point_i.sort(key=lambda x: x['distance'])
        atomic_info_list.extend(distances_from_point_i)

    return atomic_info_list
