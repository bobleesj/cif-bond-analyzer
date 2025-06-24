import numpy as np


def compute_angles_from_central_atom(CN_connections):
    """Compute the angles between vectors formed by connections from a
    central atom to its neighbors.

    Stores the calculated angles in degrees with four significant
    figures.
    """
    angles = {}

    for label, connection_data in CN_connections.items():
        angles[label] = {}
        vectors = []
        central_atom_coord = connection_data[0][2]
        # Create vectors from the central atom to each connected point
        for connection in connection_data:
            point_coord = np.array(connection[3])
            central_atom_array = np.array(central_atom_coord)
            vector = point_coord - central_atom_array
            vectors.append(vector)

        for i in range(len(vectors)):
            for j in range(i + 1, len(vectors)):
                vector_i = vectors[i]
                vector_j = vectors[j]
                dot_product = np.dot(vector_i, vector_j)
                norm_i = np.linalg.norm(vector_i)
                norm_j = np.linalg.norm(vector_j)
                cosine_angle = dot_product / (norm_i * norm_j)
                angle = np.arccos(
                    np.clip(cosine_angle, -1.0, 1.0)
                )  # Clip for safety

                angle_degrees = np.degrees(angle)
                formatted_angle = (
                    f"{angle_degrees:.4g}"  # 4 significant figures
                )

                angles[label][(i, j)] = float(formatted_angle)

    return angles


def get_largest_angle_atom_indices_largest_to_smallest(
    angles, threshold=40
) -> dict:
    """Filter and sort the angles close to 180 degrees within a
    specified threshold.

    Outputs the top 10 largest angles for each label and stores the
    pairindices of these angles.
    """
    indices = {}
    for label, angle_data in angles.items():
        # Get filtered and sorted list of (pair, angle) tuples based on the angle
        sorted_pairs = sorted(
            (
                (pair, angle)
                for pair, angle in angle_data.items()
                if abs(angle - 180) <= threshold
            ),
            # Sort by angle
            key=lambda x: x[1],
            # Largest to smallest
            reverse=True,
        )
        # Store only the pairs in the dictionary under the label
        indices[label] = [pair for pair, _ in sorted_pairs]
        # Print top 10 largest angles for each label, if available
        print(f"Largest angles for {label}:")
        for pair, angle in sorted_pairs[:10]:  # Print only top 10 angles
            print(f"  Pair: {pair}: {np.round(angle, 3)} degrees")

    return indices


def count_number_of_angles(angle_data, angle):
    """Count the occurrences of a specified angle in the angle data."""

    # Initialize count
    count = 0

    # Iterate through each angle in the dictionary
    for value in angle_data.values():
        # Check if the current angle matches the specified angle
        if value == angle:
            count += 1

    return count
