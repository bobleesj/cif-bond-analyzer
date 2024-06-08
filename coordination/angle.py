import numpy as np


def compute_angles_from_central_atom(CN_connections):
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

        # Calculate angles between each pair of vectors
        print(label)

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
                angle_degrees = np.round(np.degrees(angle), 3)
                angles[label][(i, j)] = angle_degrees

                if angle_degrees > 157:
                    print(
                        i,
                        j,
                        angle_degrees,
                        connection_data[i][2],
                        connection_data[j][2],
                    )
        print()
    return angles


def get_largest_angle_atom_indices_largest_to_smallest(
    angles, threshold=34
) -> dict:
    indicies = {}
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
        indicies[label] = [pair for pair, _ in sorted_pairs]
    return indicies
