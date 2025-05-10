def get_ring_count_above_below_central_atom_z(
    near_180_degrees_atom_indices, CN_connections
):
    """Testing purposes only."""
    ring_counts = {}
    for label, conn_data in CN_connections.items():
        # Check if there are near 180 degree connections for the label
        if not near_180_degrees_atom_indices[label]:
            continue

        # Initialize counts
        central_z_to_bottom_atom_count = 0
        central_z_to_top_atom_count = 0

        # Central atom's coordinates from the first connection
        central_atom_coord = conn_data[0][2]
        central_atom_z = central_atom_coord[2]

        # Get indices for the points that form near 180 degrees
        (
            large_angle_first_idx,
            large_angle_second_idx,
        ) = near_180_degrees_atom_indices[label][0]
        large_angle_first_idx_z = conn_data[large_angle_first_idx][3][2]
        large_angle_second_idx_z = conn_data[large_angle_second_idx][3][2]

        # Determine the more positive and more negative z values
        large_angle_higher_z_value = max(
            large_angle_first_idx_z,
            large_angle_second_idx_z,
        )
        large_angle_lower_z_value = min(
            large_angle_first_idx_z,
            large_angle_second_idx_z,
        )

        # Count atoms based on their z coordinates relative to the central atom
        for conn in conn_data:
            z = conn[3][2]
            if central_atom_z < z < large_angle_higher_z_value:
                central_z_to_top_atom_count += 1
            elif large_angle_lower_z_value < z < central_atom_z:
                central_z_to_bottom_atom_count += 1

        # Store counts in dictionary
        ring_counts[label] = {
            "top_ring_count": central_z_to_top_atom_count,
            "bottom_ring_count": central_z_to_bottom_atom_count,
        }

    return ring_counts
