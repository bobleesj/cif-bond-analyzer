from preprocess.cif_parser import get_atom_type


def compute_normalized_dists_with_methods(rad_sum, all_labels_connections):
    methods = {
        "dist_by_shortest_dist": [],
        "dist_by_CIF_rad_sum": [],
        "dist_by_CIF_rad_refined_sum": [],
        "dist_by_Pauling_rad_sum": [],
    }

    norm_dists_per_label = {}
    max_gaps_per_label = {}

    for ref_label, connection_data in all_labels_connections.items():
        # Initialize each label
        norm_dists_per_label[ref_label] = {key: [] for key in methods}
        max_gaps_per_label[ref_label] = {
            method: {"max_gap": 0, "CN": -1} for method in methods
        }
        # Limit to 20 connection data points
        connection_data = connection_data[:20]
        shortest_dist = connection_data[0][1]
        previous_values = {method: None for method in methods}

        for i, connection in enumerate(connection_data):
            connected_label = connection[0]
            # Get new rad sum for each ref label
            CIF_rad_sum_norm_value = get_rad_sum_value(
                rad_sum, "CIF_rad_sum", ref_label, connected_label
            )
            CIF_rad_sum_refined_norm_value = get_rad_sum_value(
                rad_sum, "CIF_rad_refined_sum", ref_label, connected_label
            )
            Pauling_rad_sum_norm_value = get_rad_sum_value(
                rad_sum, "Pauling_rad_sum", ref_label, connected_label
            )
            pair_dist = connection[1]
            # Compute normalized distances
            norm_dist_by_shortest_dist = compute_normalized_value(
                pair_dist, shortest_dist
            )
            norm_dist_by_CIF_rad_sum = compute_normalized_value(
                pair_dist, CIF_rad_sum_norm_value
            )
            norm_dist_by_CIF_rad_refined_sum = compute_normalized_value(
                pair_dist, CIF_rad_sum_refined_norm_value
            )
            norm_dist_by_Pauling_rad_sum = compute_normalized_value(
                pair_dist, Pauling_rad_sum_norm_value
            )

            # Store distances
            distances = {
                "dist_by_shortest_dist": norm_dist_by_shortest_dist,
                "dist_by_CIF_rad_sum": norm_dist_by_CIF_rad_sum,
                "dist_by_CIF_rad_refined_sum": norm_dist_by_CIF_rad_refined_sum,
                "dist_by_Pauling_rad_sum": norm_dist_by_Pauling_rad_sum,
            }

            for method, norm_distance in distances.items():
                norm_dists_per_label[ref_label][method].append(norm_distance)

                # Calculate and update max gaps
                if previous_values[method] is not None:
                    current_gap = round(
                        abs(norm_distance - previous_values[method]), 3
                    )
                    if (
                        current_gap
                        > max_gaps_per_label[ref_label][method]["max_gap"]
                    ):
                        max_gaps_per_label[ref_label][method][
                            "max_gap"
                        ] = current_gap
                        max_gaps_per_label[ref_label][method]["CN"] = i

                previous_values[method] = norm_distance

    return max_gaps_per_label


def compute_normalized_dists(rad_sum, all_labels_connections):
    methods = {
        "dist_by_shortest_dist": [],
    }

    norm_dists_per_label = {}
    max_gaps_per_label = {}

    for ref_label, connection_data in all_labels_connections.items():
        # Initialize each label
        norm_dists_per_label[ref_label] = {key: [] for key in methods}
        max_gaps_per_label[ref_label] = {
            method: {"max_gap": 0, "CN": -1} for method in methods
        }
        # Limit to 20 connection data points
        connection_data = connection_data[:20]
        shortest_dist = connection_data[0][1]
        previous_values = {method: None for method in methods}

        for i, connection in enumerate(connection_data):
            connected_label = connection[0]
            # Get new rad sum for each ref label

            pair_dist = connection[1]
            # Compute normalized distances
            norm_dist_by_shortest_dist = compute_normalized_value(
                pair_dist, shortest_dist
            )

            # Store distances
            distances = {
                "dist_by_shortest_dist": norm_dist_by_shortest_dist,
            }

            for method, norm_distance in distances.items():
                norm_dists_per_label[ref_label][method].append(norm_distance)

                # Calculate and update max gaps
                if previous_values[method] is not None:
                    current_gap = round(
                        abs(norm_distance - previous_values[method]), 3
                    )
                    if (
                        current_gap
                        > max_gaps_per_label[ref_label][method]["max_gap"]
                    ):
                        max_gaps_per_label[ref_label][method][
                            "max_gap"
                        ] = current_gap
                        max_gaps_per_label[ref_label][method]["CN"] = i

                previous_values[method] = norm_distance

    return max_gaps_per_label


def compute_normalized_value(number, ref_number):
    return round((number / ref_number), 5)


def get_rad_sum_value(rad_sum, method_name, ref_label, other_label):
    ref_element = get_atom_type(ref_label)
    other_element = get_atom_type(other_label)
    return rad_sum[method_name][f"{ref_element}-{other_element}"]
