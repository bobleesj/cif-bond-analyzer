import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import Delaunay
from scipy.spatial import ConvexHull
from coordination.angle import count_number_of_angles


def plot_polyhedrons(
    near_180_degrees_atom_indices,
    angles,
    CN_connections,
    file_path,
):
    file_name = os.path.basename(file_path)

    """
    Plot the best polyhedron for each label using 3D visualization with
    Poly3DCollection.

    *Not used in CBA at the moment. This is for testing purposes only.    
    """
    color_map = {
        "In1": "blue",
        "U1": "green",
        "Rh1": "yellow",
        "Rh2": "purple",
        "Mo1A": "red",
        "Os1B": "red",
        "Mo2A": "teal",
        "Os2B": "teal",
        "Mo3A": "magenta",
        "Os3B": "magenta",
        "Mo4A": "cyan",
        "Os4B": "cyan",
        "Mo5A": "olive",
        "Os5B": "olive",
        "Ni": "blue",
        "Ta3": "purple",
        "Ta2": "purple",
        "Ta1": "purple",
    }

    for label, conn_data in CN_connections.items():
        conn_data = CN_connections[label]
        CN = len(conn_data)
        # List of points forming the polyhedron
        polyhedron_points = [conn[3] for conn in conn_data]
        vertex_labels = [conn[0] for conn in conn_data]

        # Central atom's coordinates and label from the first connection
        central_atom_coord = conn_data[0][2]
        central_atom_label = label
        polyhedron_points.append(central_atom_coord)
        vertex_labels.append(central_atom_label)
        polyhedron_points_array = np.array(polyhedron_points)

        # Set up the plot
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection="3d")
        hull = ConvexHull(polyhedron_points_array)
        # Draw each edge individually
        for simplex in hull.simplices:
            for i in range(len(simplex)):
                start_point = simplex[i]
                end_point = simplex[(i + 1) % len(simplex)]
                x_line = [
                    polyhedron_points_array[start_point, 0],
                    polyhedron_points_array[end_point, 0],
                ]
                y_line = [
                    polyhedron_points_array[start_point, 1],
                    polyhedron_points_array[end_point, 1],
                ]
                z_line = [
                    polyhedron_points_array[start_point, 2],
                    polyhedron_points_array[end_point, 2],
                ]
                ax.plot(
                    x_line,
                    y_line,
                    z_line,
                    "k-",
                    alpha=0.5,
                    linewidth=1.5,
                )

        # Use Poly3DCollection to draw faces with specified alpha and facecolor
        poly3d = [polyhedron_points_array[simplex] for simplex in hull.simplices]
        poly_collection = Poly3DCollection(poly3d, alpha=0.1, facecolor="cyan")
        ax.add_collection3d(poly_collection)

        # Plot and label vertices with colors based on labels
        for i, point in enumerate(polyhedron_points_array):
            label = vertex_labels[i]
            color = color_map.get(
                label, "grey"
            )  # Use grey as a default color if label is not found
            ax.scatter(*point, color=color, s=350)
            ax.text(
                *point,
                f"{label}-{i}",
                color="black",
                alpha=1,
                fontsize=12,
                zorder=3,
            )

        # Set labels and title
        ax.set_title(f"Best Polyhedron for {label}. CN={len(conn_data)}, {file_name}")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.set_zlabel("Z Coordinate")
        # ax.autoscale_view()
        # ax.set_axis_off()  # Hide the axes, as requested

        """
        Step 1. Find the largest angle indices ref from the central atom
        """
        largest_angle_index_pair = near_180_degrees_atom_indices[label][0]

        largest_angle = angles[label][largest_angle_index_pair]
        large_angle_index_1 = largest_angle_index_pair[0]
        large_angle_index_2 = largest_angle_index_pair[1]
        large_angle_index_1_coord = conn_data[large_angle_index_1][3]
        large_angle_index_2_coord = conn_data[large_angle_index_2][3]
        ax.scatter(
            *large_angle_index_1_coord,
            color="black",
            s=1000,
        )  # Larger size for visibility
        ax.scatter(
            *large_angle_index_2_coord,
            color="black",
            s=1000,
        )

        # Distance and angle counts
        angle_180_count = count_number_of_angles(angles[label], 180.0)
        first_shortest_dist_count = nth_shortest_distance_count(
            CN_connections, label, 0
        )
        second_shortest_dist_count = nth_shortest_distance_count(
            CN_connections, label, 1
        )

        """
        Type 10.1. 180, CN=10, top 4, bottom 4, 180 largest angle
        """
        if CN == 10 and largest_angle == 180.0:
            top_box_vertices = draw_rectangular_box(
                ax,
                central_atom_coord,
                large_angle_index_1_coord,
                "blue",
            )
            count_atoms_inside_polyhedron(top_box_vertices, polyhedron_points_array)

            # Draw the other box with the largest angle
            bottom_box_vertices = draw_rectangular_box(
                ax,
                central_atom_coord,
                large_angle_index_2_coord,
                "red",
            )

            count_atoms_inside_polyhedron(bottom_box_vertices, polyhedron_points_array)

        """
        Type 12.1. 180, CN=12, top 5, bottom 5
        """
        if CN == 12:
            print(
                angle_180_count,
                first_shortest_dist_count,
                second_shortest_dist_count,
            )
            if (
                angle_180_count == 3
                and first_shortest_dist_count == 6
                and second_shortest_dist_count == 6
            ):
                print("CN 12 (Cuboctahedron")

            elif (
                angle_180_count == 6
                and first_shortest_dist_count == 6
                and second_shortest_dist_count == 6
            ):
                print("CN 12 (anticuboctahedron")
            else:
                print("Type 2. 180, CN=12, top 5, bottom 5")
                top_box_vertices = draw_rectangular_box(
                    ax,
                    central_atom_coord,
                    large_angle_index_1_coord,
                    "blue",
                )
                count_atoms_inside_polyhedron(
                    top_box_vertices,
                    polyhedron_points_array,
                )
                bottom_box_vertices = draw_rectangular_box(
                    ax,
                    central_atom_coord,
                    large_angle_index_2_coord,
                    "red",
                )

                count_atoms_inside_polyhedron(
                    bottom_box_vertices,
                    polyhedron_points_array,
                )
                print()

            """
            Type 12.2. 3 180 angles, 6 1st shortest dists, 6 2nd shortest dists
            """

        if CN == 14:
            if (
                angle_180_count == 7
                and first_shortest_dist_count == 8
                and second_shortest_dist_count == 6
            ):
                """
                Type 14.2 rhombic dodecahedron, 8 identical shortest distances,
                7 of 180 degree angles.
                Assume it has no distortion at the moment
                """
                print("Type 14.2 rhombic")

            elif largest_angle > 178.0:
                """
                Type 14.1. 180, CN=14, top 6, bottom 6
                """
                print("\nType 14.1. 180, CN=14, top 6, bottom 6")

                top_box_vertices = draw_rectangular_box(
                    ax,
                    central_atom_coord,
                    large_angle_index_1_coord,
                    "blue",
                )
                count_atoms_inside_polyhedron(
                    top_box_vertices,
                    polyhedron_points_array,
                )
                # Draw the other box with the largest angle

                bottom_box_vertices = draw_rectangular_box(
                    ax,
                    central_atom_coord,
                    large_angle_index_2_coord,
                    "red",
                )

                count_atoms_inside_polyhedron(
                    bottom_box_vertices,
                    polyhedron_points_array,
                )

        if CN == 15:
            largest_angle_pair = near_180_degrees_atom_indices[label][0]
            second_largest_angle_pair = near_180_degrees_atom_indices[label][1]
            """
            ***Type 15.1. 157.037 CN=15, top 6, bottom (two split) 5***
            The two largest angle pairs have pairs like, (2, 13), (2, 14).
            
            Pair: (2, 13): 157.0 degrees
            Pair: (2, 14): 157.0 degrees
            Pair: (0, 9): 156.5 degrees

            13 and 14 must be the two split atoms. Find the average position between 13 and 14,
            draw a box from the central atom to the average position between 13, 14
            """

            if largest_angle_pair[0] == second_largest_angle_pair[0]:
                print("\nType 15.1. 157.037 CN=15, top 6, bottom (two split) 6")
                # Use the function
                (
                    top_point_index,
                    split_atom_point_1_index,
                    split_atom_point_2_index,
                ) = find_common_and_unique_points(
                    largest_angle_pair,
                    second_largest_angle_pair,
                )

                point_1 = polyhedron_points_array[split_atom_point_1_index]
                point_2 = polyhedron_points_array[split_atom_point_2_index]
                single_largest_angle_coord = polyhedron_points_array[top_point_index]
                # Calculate the average position (midpoint)
                average_split_coord = (point_1 + point_2) / 2

                top_box_vertices = draw_rectangular_box(
                    ax,
                    central_atom_coord,
                    single_largest_angle_coord,
                    "cyan",
                )
                count_atoms_inside_polyhedron(
                    top_box_vertices,
                    polyhedron_points_array,
                )
                # Draw the other box with the largest angle

                bottom_box_vertices = draw_rectangular_box(
                    ax,
                    central_atom_coord,
                    average_split_coord,
                    "purple",
                )

                count_atoms_inside_polyhedron(
                    bottom_box_vertices,
                    polyhedron_points_array,
                    split_count=2,
                )

            """
            ***Type 15.2. Symmetric case where there are 3 largest angles formed
            by the single atom and one of the two-split atoms
            Largest angles for Ta2:
            Pair: (6, 10): 154.3 degrees
            Pair: (7, 11): 154.3 degrees
            Pair: (8, 9): 154.3 degrees
            """
            largest_angle_pair = near_180_degrees_atom_indices[label][0]
            second_largest_angle_pair = near_180_degrees_atom_indices[label][1]
            thrid_largest_angle_pair = near_180_degrees_atom_indices[label][2]
            largest_angle = angles[label][largest_angle_pair]
            second_largest_angle = angles[label][second_largest_angle_pair]
            third_largest_angle = angles[label][thrid_largest_angle_pair]

            if largest_angle == second_largest_angle == third_largest_angle:
                print(
                    "\nType 15.2. CN=15, top 6, bottom (two split) 6, 3 identical largest angles"
                )
                single_largest_angle_coord = polyhedron_points_array[
                    # Pair: (6, 10): 154.3 degrees
                    largest_angle_pair[0]
                ]

                # Pair: (6, 13): 153.3 degrees
                # Find the largest angle ex) from 6 to 13
                # But this sorted by the distance and also by the pair
                """
                Largest angles for Ta2:
                Pair: (6, 10): 154.3 degrees
                Pair: (7, 11): 154.3 degrees
                Pair: (8, 9): 154.3 degrees
                Pair: (6, 13): 153.3 degrees <-
                Pair: (7, 14): 153.3 degrees
                Pair: (8, 12): 153.3 degrees
                """
                other_double_split_atom_index = near_180_degrees_atom_indices[label][3][
                    1
                ]
                # Find the average position between the two atoms in the doublet
                first_double_split_atom_index = largest_angle_pair[1]
                point_1 = polyhedron_points_array[first_double_split_atom_index]
                point_2 = polyhedron_points_array[other_double_split_atom_index]
                average_split_coord = (point_1 + point_2) / 2

                # Get the two from the top atom to other
                top_box_vertices = draw_rectangular_box(
                    ax,
                    central_atom_coord,
                    single_largest_angle_coord,
                    "red",
                )
                count_atoms_inside_polyhedron(
                    top_box_vertices,
                    polyhedron_points_array,
                )
                # Draw the other box with the largest angle

                bottom_box_vertices = draw_rectangular_box(
                    ax,
                    central_atom_coord,
                    average_split_coord,
                    "purple",
                )

                count_atoms_inside_polyhedron(
                    bottom_box_vertices,
                    polyhedron_points_array,
                    split_count=2,
                )

        if CN == 16:
            fourth_largest_angle_pair_indicies = near_180_degrees_atom_indices[label][3]
            fifth_largest_angle_pair_indicies = near_180_degrees_atom_indices[label][4]
            sixth_largest_angle_pair_indicies = near_180_degrees_atom_indices[label][5]

            """
            
            Type 16.1. 3 splits, CN=16, Ta1 in 20250604_CN_4_methods/457848.cif
            - Check there are CN=16
            - 3 angles formed 159.7
            - 6 angles formed 148.7
            - 3 angles formde 149.4
            Largest angles for Ta1:
            Pair: (4, 8): 159.7 degrees
            Pair: (5, 9): 159.7 degrees
            Pair: (6, 7): 159.7 degrees
            Pair: (0, 1): 149.4 degrees
            Pair: (0, 2): 149.4 degrees
            Pair: (0, 3): 149.4 degrees
            Pair: (1, 10): 148.7 degrees
            Pair: (1, 14): 148.7 degrees
            Pair: (2, 11): 148.7 degrees
            Pair: (2, 12): 148.7 degrees
            Check the triplets - this is the second largest angles, ther are 3 of them
            Assume the the bottom is the 3 splits, the top forms a 6 ring chain
            The bottom forms 
            (0, 2) (0, 3) (0, 1), 0th index must be the top atom
            """
            if (
                fourth_largest_angle_pair_indicies[0]
                == fifth_largest_angle_pair_indicies[0]
                == sixth_largest_angle_pair_indicies[0]
            ):
                """
                Draw a box that encompasses 6 atoms at the top ring
                """
                print("Type 16.1 CN=16, top 6, bottom (three splits) 6")
                # Draw top box with no split

                top_box_vertices = draw_rectangular_box(
                    ax,
                    central_atom_coord,
                    polyhedron_points_array[fourth_largest_angle_pair_indicies[0]],
                    "blue",
                )
                count_atoms_inside_polyhedron(
                    top_box_vertices,
                    polyhedron_points_array,
                    split_count=1,
                )
                # Draw bottom box with 3 splits
                triple_split_coord_1 = polyhedron_points_array[
                    fourth_largest_angle_pair_indicies[1]
                ]
                triple_split_coord_2 = polyhedron_points_array[
                    fifth_largest_angle_pair_indicies[1]
                ]
                triple_split_coord_3 = polyhedron_points_array[
                    sixth_largest_angle_pair_indicies[1]
                ]
                average_split_coord = (
                    triple_split_coord_1 + triple_split_coord_2 + triple_split_coord_3
                ) / 3
                bottom_box_vertices = draw_rectangular_box(
                    ax,
                    central_atom_coord,
                    average_split_coord,
                    "red",
                )
                count_atoms_inside_polyhedron(
                    bottom_box_vertices,
                    polyhedron_points_array,
                    split_count=3,
                )
        plt.show()


# Function to find common and unique points
def find_common_and_unique_points(pair1, pair2):
    if pair1[0] == pair2[0]:
        return pair1[0], pair1[1], pair2[1]
    elif pair1[0] == pair2[1]:
        return pair1[0], pair1[1], pair2[0]
    elif pair1[1] == pair2[0]:
        return pair1[1], pair1[0], pair2[1]
    elif pair1[1] == pair2[1]:
        return pair1[1], pair1[0], pair2[0]
    else:
        raise ValueError("No common point found")


def draw_rectangular_box(
    ax,
    central_atom_coord,
    large_angle_index_1_coord,
    color,
    scale_factor=1.1,
    extension_factor=1.05,
):
    """
    Draw a rectangular box with a slight extension and scaling to
    ensure coverage of additional space.
    """

    # Calculate the line vector
    line_vector = np.array(large_angle_index_1_coord) - np.array(central_atom_coord)
    line_vector *= extension_factor  # Extend the line vector slightly
    large_angle_index_1_coord = (
        central_atom_coord + line_vector
    )  # Recalculate the end point coordinate

    norm_value = 3
    # Handling special case where the line vector is vertical or aligned with any axis
    if np.all(line_vector[:2] == 0):  # Line is vertical (change in z only)
        # Choose arbitrary perpendicular vectors in the XY plane
        half_width_vector = np.array([norm_value, 0, 0], dtype=np.float64)
        half_height_vector = np.array([0, norm_value, 0], dtype=np.float64)
    else:
        # General case, generate vectors not aligned with the line vector
        if line_vector[0] == 0:
            half_width_vector = np.array([1, 0, 0], dtype=np.float64)
        else:
            half_width_vector = np.array(
                [-line_vector[1], line_vector[0], 0],
                dtype=np.float64,
            )

        half_width_vector /= np.linalg.norm(half_width_vector)
        half_height_vector = np.cross(line_vector, half_width_vector)
        half_height_vector /= np.linalg.norm(half_height_vector)

    # Scale for visibility and additional coverage
    half_width_vector *= norm_value * scale_factor
    half_height_vector *= norm_value * scale_factor

    # Calculate vertices of the box
    vertices = np.array(
        [
            central_atom_coord - half_width_vector - half_height_vector,
            central_atom_coord + half_width_vector - half_height_vector,
            central_atom_coord - half_width_vector + half_height_vector,
            central_atom_coord + half_width_vector + half_height_vector,
            large_angle_index_1_coord - half_width_vector - half_height_vector,
            large_angle_index_1_coord + half_width_vector - half_height_vector,
            large_angle_index_1_coord - half_width_vector + half_height_vector,
            large_angle_index_1_coord + half_width_vector + half_height_vector,
        ]
    )

    # Plot the original line
    ax.plot(
        [
            central_atom_coord[0],
            large_angle_index_1_coord[0],
        ],
        [
            central_atom_coord[1],
            large_angle_index_1_coord[1],
        ],
        [
            central_atom_coord[2],
            large_angle_index_1_coord[2],
        ],
        color="blue",
    )

    # Draw lines connecting the vertices to form the box
    for start, end in [
        (0, 1),
        (0, 2),
        (1, 3),
        (2, 3),  # Bottom face
        (4, 5),
        (4, 6),
        (5, 7),
        (6, 7),  # Top face
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),  # Sides
    ]:
        ax.plot(
            [vertices[start][0], vertices[end][0]],
            [vertices[start][1], vertices[end][1]],
            [vertices[start][2], vertices[end][2]],
            color=color,
        )

    return vertices


def is_inside_convex_polyhedron(point, vertices):
    """
    Check if a point is inside a convex polyhedron defined by
    its vertices using Delaunay triangulation.
    """
    hull = Delaunay(vertices)
    return hull.find_simplex(point) >= 0


def count_atoms_inside_polyhedron(vertices, atom_positions, split_count=1):
    """
    Counts how many atoms are inside the convex polyhedron defined by vertices.
    """
    count = 0
    for i, pos in enumerate(atom_positions):
        if is_inside_convex_polyhedron(pos, vertices):
            count += 1
    if split_count == 1:
        count_subtracted_central_large_angle = count - 2
    if split_count == 2:
        count_subtracted_central_large_angle = count - 3
    if split_count == 3:
        count_subtracted_central_large_angle = count - 4
    print(f"Number of atoms inside the box: {count_subtracted_central_large_angle}")
    return count_subtracted_central_large_angle
