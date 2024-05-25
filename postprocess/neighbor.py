import json
import os
import pandas as pd
import numpy as np
from preprocess import supercell


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


def print_conneted_points(all_labels_connections):
    # Print all collected results
    print("All labels and their most connected points:")
    for label, connections in all_labels_connections.items():
        print(f"\nAtom site {label}:")
        for (
            label,
            dist,
            coords_1,
            coords_2,
            diff,
        ) in connections:
            print(f"{label} {dist} {coords_1}, {coords_2}, {diff}")
    print()


def filter_connections_with_CN(
    labels_connections, nearest_neighbor_max_count=20
):
    """
    Reduces the number of connections based on the CN
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
            print(max_gap_index)
            filtered_connections[label] = limited_label_data[:max_gap_index]

    return filtered_connections


def calculate_normalized_distances(connections):
    """
    Calculate normalized distances for each connection
    """
    min_dist = connections[0][1]
    normalized_distances = [
        np.round(dist / min_dist, 3) for _, dist, _, _ in connections
    ]
    return normalized_distances


def calculate_normalized_dist_diffs(normalized_distances):
    """
    Calculate differences between consecutive normalized distances
    """
    normalized_dist_diffs = [
        normalized_distances[k + 1] - normalized_distances[k]
        for k in range(len(normalized_distances) - 1)
    ]
    return normalized_dist_diffs


def add_diff_after(all_labels_connections):
    """
    Add the diff_after value to each connection
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


def save_to_excel_json(all_labels_connections, output_folder, filename):
    """
    Saves the connection data for each label to an Excel file
    """
    # Save Excel
    excel_file_path = os.path.join(output_folder, filename + ".xlsx")
    # Create an Excel writer object using pandas
    with pd.ExcelWriter(excel_file_path, engine="openpyxl") as writer:
        for label, connections in all_labels_connections.items():
            if connections:
                # Convert the connection data into a DataFrame
                df = pd.DataFrame(
                    connections,
                    columns=[
                        "site_label",
                        "distance_angstrom",
                        "coord_1",
                        "coord_2",
                        "norm_diff",
                    ],
                )
                # df = df.drop(columns=["coord_1", "coord_2"])
                # Write the DataFrame to an Excel sheet named after the label
                df.to_excel(writer, sheet_name=label, index=False)
                print(f"Data for {label} saved to Excel sheet.")
            else:
                print(f"No data available for {label}, no sheet created.")

    # Save to JSON
    json_file_path = os.path.join(output_folder, filename + ".json")
    with open(json_file_path, "w") as json_file:
        json.dump(all_labels_connections, json_file, indent=4)
    print(f"Data saved to JSON file: {json_file_path}")


def save_text_file(
    all_labels_connections, output_folder, filename, is_CN_used
):
    """
    Saves the connection data for each label to an .txt file
    """
    text_file_path = os.path.join(output_folder, filename + ".txt")
    is_verbose_output = True

    # Define field widths
    label_width = 5
    dist_width = 7
    coord_width = 23
    norm_diff_width = 10

    if is_verbose_output:
        filename += "_v"

    text_file_path = os.path.join(output_folder, filename + ".txt")

    # Create the text file
    with open(text_file_path, "w") as text_file:
        for label, connections in all_labels_connections.items():
            top_label = (
                f"{label} CN:{len(connections)}"
                if is_CN_used
                else f"{label} count:{len(connections)}"
            )
            if connections:
                text_file.write(f"{top_label}\n")
                for connection in connections:
                    (
                        site_label,
                        distance,
                        coord_1,
                        coord_2,
                        norm_diff,
                    ) = connection

                    # Format coordinates and norm_diff to 3 decimal places
                    coord_1_str = ", ".join(f"{c:.3f}" for c in coord_1)
                    coord_2_str = ", ".join(f"{c:.3f}" for c in coord_2)
                    distance_str = f"{distance:.3f}"
                    norm_diff_str = (
                        f"{norm_diff:.3f}" if norm_diff is not None else ""
                    )

                    if is_verbose_output:
                        text_file.write(
                            f"{site_label:<{label_width}} dist: {distance_str:<{dist_width}} "
                            f"coord 1: {coord_1_str:<{coord_width}} coord 2: {coord_2_str:<{coord_width}} "
                            f"norm_diff: {norm_diff_str:<{norm_diff_width}}\n"
                        )
                    else:
                        text_file.write(
                            f"{site_label:<{label_width}} {distance_str:<{dist_width}}\n"
                        )
                text_file.write("\n")
            else:
                text_file.write(f"No data available for {label}\n\n")

    print(f"Data saved to text file: {text_file_path}")
