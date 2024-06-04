import numpy as np
from preprocess import supercell


def calculate_normalized_dist_diffs(normalized_distances):
    """
    Calculates differences between consecutive normalized distances.
    """
    normalized_dist_diffs = [
        normalized_distances[k + 1] - normalized_distances[k]
        for k in range(len(normalized_distances) - 1)
    ]
    return normalized_dist_diffs


def add_diff_after(all_labels_connections):
    """
    Adds the diff_after value to each connection.
    """
    updated_connections = {}
    for label, connections in all_labels_connections.items():
        updated_connections[label] = []

        # Calculate normalized distances and their differences
        normalized_distances = calculate_normalized_distances(connections)
        normalized_dist_diffs = calculate_normalized_dist_diffs(
            normalized_distances
        )

        for idx, (conn_label, dist, coord_1, coord_2) in enumerate(
            connections
        ):
            if idx < len(connections) - 1:
                diff_after = (
                    np.round(normalized_dist_diffs[idx], 3)
                    if idx < len(normalized_dist_diffs)
                    else None
                )
                updated_connections[label].append(
                    (conn_label, dist, coord_1, coord_2, diff_after)
                )

    return updated_connections


def get_most_connected_point_per_site(label, dist_dict, dist_set):
    """
    Identifies the reference point with the highest number of connections
    within the shortest distances from a set of distances.
    """
    sorted_unique_dists = sorted(dist_set)
    # Get the 7 shortest distances
    shortest_dists = sorted_unique_dists[:7]

    # Variables to track the reference point with the highest count
    max_count = 0
    max_ref_point = None
    max_connections = []

    for ref_idx, connections in dist_dict.items():
        # Initialize a dictionary to count occurrences of each shortest
        dist_counts = {dist: 0 for dist in shortest_dists}

        # Count the occurrences of the shortest distances
        for _, dist, _, _ in connections:
            if dist in dist_counts:
                dist_counts[dist] += 1

        # Calculate the total count of occurrences for this reference point
        total_count = sum(dist_counts.values())

        # Check if this is the maximum we've encountered so far
        if total_count > max_count:
            max_count = total_count
            max_ref_point = ref_idx
            max_connections = sorted(connections, key=lambda x: x[1])

    # Return the max point
    if max_ref_point is not None:
        return label, [
            (other_label, dist, cart_1, cart_2)
            for other_label, dist, cart_1, cart_2 in max_connections
        ]


def get_nearest_dists_per_site(
    filtered_unitcell_points,
    supercell_points,
    cutoff_radius,
    lengths,
    angles_rad,
):
    # Initialize a dictionary to store the relationships
    dist_dict = {}
    dist_set = set()

    # Loop through each point in the filtered list
    for i, point_1 in enumerate(filtered_unitcell_points):
        point_2_info = []
        for j, point_2 in enumerate(supercell_points):
            if point_1 == point_2:
                continue  # Skip comparison with itself
            # Convert fractional to Cartesian coordinates
            cart_1 = supercell.fractional_to_cartesian(
                [point_1[0], point_1[1], point_1[2]],
                lengths,
                angles_rad,
            )
            cart_2 = supercell.fractional_to_cartesian(
                [point_2[0], point_2[1], point_2[2]],
                lengths,
                angles_rad,
            )

            # Calculate the dist between two points
            dist = supercell.calc_dist_two_cart_points(cart_1, cart_2)
            dist = np.round(dist, 3)

            # Check the dist
            if dist < cutoff_radius and dist > 0.1:
                point_2_info.append(
                    (
                        point_2[3],  # site label
                        dist,
                        [
                            np.round(cart_1[0], 3),  # x
                            np.round(cart_1[1], 3),  # y
                            np.round(cart_1[2], 3),  # z
                        ],
                        [
                            np.round(cart_2[0], 3),  # x
                            np.round(cart_2[1], 3),  # y
                            np.round(cart_2[2], 3),  # z
                        ],
                    )
                )
            dist_set.add(dist)
        # Store the list in the dictionary with `i` as the key
        if point_2_info:
            dist_dict[i] = point_2_info

    return dist_dict, dist_set


def get_all_labels_connections(
    labels,
    unitcell_points,
    supercell_points,
    cutoff_radius,
    lengths,
    angles,
    is_cn_used,
):
    """
    Computes all pair distances per site label.
    """
    all_labels_connections = {}
    for site_label in labels:
        filtered_unitcell_points = [
            point for point in unitcell_points if point[3] == site_label
        ]

        dist_result = get_nearest_dists_per_site(
            filtered_unitcell_points,
            supercell_points,
            cutoff_radius,
            lengths,
            angles,
        )

        dist_dict, dist_set = dist_result

        (
            label,
            connections,
        ) = get_most_connected_point_per_site(site_label, dist_dict, dist_set)

        all_labels_connections[label] = connections

    # Determine coordination number
    if is_cn_used:
        all_labels_connections = filter_connections_with_cn(
            all_labels_connections
        )

    all_labels_connections = add_diff_after(all_labels_connections)
    return all_labels_connections


def filter_connections_with_cn(
    labels_connections, nearest_neighbor_max_count=20
):
    """
    Reduces the number of connections based on the CN.
    """
    filtered_connections = {}
    for label, label_data in labels_connections.items():
        # Limit to the first nearest_neighbor_max_count distances
        limited_label_data = label_data[:nearest_neighbor_max_count]

        if not limited_label_data:
            continue

        # Calculate normalized distances
        normalized_distances = calculate_normalized_distances(
            limited_label_data
        )

        # Calculate diffs between consecutive normalized distances
        normalized_dist_diffs = calculate_normalized_dist_diffs(
            normalized_distances
        )

        # Find the maximum gap and its position
        if normalized_dist_diffs:
            max_gap = max(normalized_dist_diffs)
            max_gap_index = normalized_dist_diffs.index(max_gap) + 2
            filtered_connections[label] = limited_label_data[:max_gap_index]

    return filtered_connections


def calculate_normalized_distances(connections):
    """
    Calculates normalized distances for each connection
    """
    min_dist = connections[0][1]
    normalized_distances = [
        np.round(dist / min_dist, 3) for _, dist, _, _ in connections
    ]
    return normalized_distances
