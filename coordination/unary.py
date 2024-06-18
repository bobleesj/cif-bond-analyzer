import numpy as np
from coordination import handler as cn_handler
from coordination import unary as cn_unary
from coordination import calculator as cn_calculator
from util import folder


def compute_shortest_distance_for_unary(connected_points):
    if not len(connected_points) == 1:
        return None

    # Directly access the first and only item in the dictionary
    first_key = next(iter(connected_points))
    return connected_points[first_key][0][1]


def compute_average_radius_by_shortest_dist(
    connected_points_group,
):
    element_shortest_dists = []
    for connected_points in connected_points_group:
        # Compute the shortest distance for the file
        shortest_dist = (
            cn_unary.compute_shortest_distance_for_unary(
                connected_points
            )
        )
        element_shortest_dists.append(shortest_dist)

    rads = np.array(element_shortest_dists) / 2
    avg_rad = np.round(np.average(rads), 3)

    # print("Rads:", rads)
    # print("Average_radius:", avg_rad)
    if element_shortest_dists:
        return avg_rad
    else:
        return 0


def get_coordination_number_by_dist_min(
    connected_points_group,
):
    """
    Computes the largest gap index for each group of connected points based on the shortest distance.
    """
    largest_gap_indices = []

    for connected_points in connected_points_group:
        first_key = next(iter(connected_points))
        connection_data = connected_points[first_key]

        # Consider the first 20 only, or all if fewer than 20
        connection_data = connection_data[:20]
        shortest_dist = connection_data[0][1]

        previous_norm_dist = None
        largest_gap = 0
        largest_gap_index = 0

        for i, connection in enumerate(connection_data):
            pair_dist = connection[1]
            norm_dist_by_shortest_dist = (
                cn_calculator.compute_normalized_value(
                    pair_dist, shortest_dist
                )
            )
            # Calculate the gap and update if this gap is the largest seen
            if previous_norm_dist is not None:
                gap = abs(
                    norm_dist_by_shortest_dist
                    - previous_norm_dist
                )
                if gap > largest_gap:
                    largest_gap = gap
                    largest_gap_index = i

            previous_norm_dist = norm_dist_by_shortest_dist

        # Store the largest gap index for this group of connected points
        largest_gap_indices.append(largest_gap_index)

    return int(np.median(largest_gap_indices))


def find_avg_radius_from_avg_dist_from_central_atom(
    coordination_number, connected_points_group
):
    avg_dists_from_central_atom = []

    # Process for each conncetion points per file
    for connected_points in connected_points_group:
        first_key = next(iter(connected_points))
        all_dist_avg_per_file = 0.0

        # Find the average dist from the central atom to all other
        # points in the coordination number
        for connection_data in connected_points[first_key][
            :coordination_number
        ]:
            all_dist_avg_per_file += float(
                connection_data[1]
            )

        avg_dists_from_central_atom.append(
            all_dist_avg_per_file / coordination_number
        )
    avg_radius = round(
        np.mean(avg_dists_from_central_atom) / 2, 3
    )
    return avg_radius
