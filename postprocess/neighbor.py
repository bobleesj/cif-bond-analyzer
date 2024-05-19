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

            # If dist is within the specified limit, append
            if dist < cutoff_radius:
                point_2_info.append((j, point_2[3], dist))
            dist_set.add(dist)
        # Store the list in the dictionary with `i` as the key
        if (
            point_2_info
        ):  # Only add to dictionary if there are close points
            dist_dict[i] = point_2_info

    return dist_dict, dist_set


def get_most_connected_point(label, dist_dict, dist_set):
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
        for _, _, dist in connections:
            if dist in dist_counts:
                dist_counts[dist] += 1

        # Calculate the total count of occurrences for this reference point
        total_count = sum(dist_counts.values())

        # Check if this is the maximum we've encountered so far
        if total_count > max_count:
            max_count = total_count
            max_ref_point = ref_idx
            max_connections = sorted(connections, key=lambda x: x[2])

    # After determining the max, print the with the max count
    if max_ref_point is not None:
        return label, [
            (other_label, dist)
            for _, other_label, dist in max_connections
        ]


def print_conneted_points(all_labels_connections):
    # Print all collected results
    print("All labels and their most connected points:")
    for label, connections in all_labels_connections.items():
        print(f"\nAtom site {label}:")
        for label, dist in connections:
            print(f"{label} {dist}")
    print()


def save_to_excel(all_labels_connections, filename):
    """
    Saves the connection data for each label to an Excel file
    """
    # Create an Excel writer object using pandas
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        for label, connections in all_labels_connections.items():
            if (
                connections
            ):  # Check if there are any connections to save
                # Convert the connection data into a DataFrame
                df = pd.DataFrame(
                    connections,
                    columns=["site_label", "distance_angstrom"],
                )
                # Write the DataFrame to an Excel sheet named after the label
                df.to_excel(writer, sheet_name=label, index=False)
                print(f"Data for {label} saved to Excel sheet.")
            else:
                print(
                    f"No data available for {label}, no sheet created."
                )
