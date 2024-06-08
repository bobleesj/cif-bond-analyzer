import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import Delaunay


def plot_polyhedrons(near_180_degrees_atom_indices, angles, CN_connections):
    """
    Plot the best polyhedron for each label using 3D visualization with
    Poly3DCollection.
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
    }

    for label, conn_data in CN_connections.items():
        if not near_180_degrees_atom_indices[label]:
            continue

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
                ax.plot(x_line, y_line, z_line, "k-", alpha=0.5, linewidth=1.5)

        # Use Poly3DCollection to draw faces with specified alpha and facecolor
        poly3d = [
            polyhedron_points_array[simplex] for simplex in hull.simplices
        ]
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
        ax.set_title(f"Best Polyhedron for {label}. CN={len(conn_data)}")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.set_zlabel("Z Coordinate")
        ax.autoscale_view()
        # ax.set_axis_off()  # Hide the axes, as requested

        """
        Step 1. Find the largest angle indices ref from the central atom
        """
        largest_angle_index_pair = near_180_degrees_atom_indices[label][0]
        """
        Type 1. 180, CN=14, top 6, bottom 6
        Type 2. 180, CN=12, top 5, bottom 5
        """
        largest_angle = angles[label][largest_angle_index_pair]
        if largest_angle > 178.0:
            large_angle_index_1 = largest_angle_index_pair[0]
            large_angle_index_2 = largest_angle_index_pair[1]
            large_angle_index_1_coord = conn_data[large_angle_index_1][3]
            large_angle_index_2_coord = conn_data[large_angle_index_2][3]
            ax.scatter(
                *large_angle_index_1_coord, color="black", s=1000
            )  # Larger size for visibility
            ax.scatter(*large_angle_index_2_coord, color="black", s=1000)

            """
            Step 2. Draw boxes above and below
            """

            print(label)
            top_box_vertices = draw_rectangular_box(
                ax, central_atom_coord, large_angle_index_1_coord, "blue"
            )
            count_atoms_inside_polyhedron(
                top_box_vertices, polyhedron_points_array
            )
            # Draw the other box with the largest angle

            bottom_box_vertices = draw_rectangular_box(
                ax, central_atom_coord, large_angle_index_2_coord, "red"
            )

            count_atoms_inside_polyhedron(
                bottom_box_vertices, polyhedron_points_array
            )
            print()
        """
        Type 3. 157.037 CN=15, top 6, bottom (two split) 5
        """
        if largest_angle > 157 and largest_angle < 158:
            print("Type 3. 157.037 CN=15, top 6, bottom (two split) 6")
            angle_pair_1 = near_180_degrees_atom_indices[label][0]
            angle_pair_2 = near_180_degrees_atom_indices[label][1]

            # Use the function
            (
                top_point_index,
                split_atom_point_1_index,
                split_atom_point_2_index,
            ) = find_common_and_unique_points(angle_pair_1, angle_pair_2)

            print(
                top_point_index,
                split_atom_point_1_index,
                split_atom_point_2_index,
            )

            """
            Find the average position between split_atom_point_1_index_coord 
            and split_atom_point_2_coord
            """
            point_1 = polyhedron_points_array[split_atom_point_1_index]
            point_2 = polyhedron_points_array[split_atom_point_2_index]
            single_largest_angle_coord = polyhedron_points_array[
                top_point_index
            ]
            # Calculate the average position (midpoint)
            average_split_coord = (point_1 + point_2) / 2

            top_box_vertices = draw_rectangular_box(
                ax, central_atom_coord, single_largest_angle_coord, "cyan"
            )
            count_atoms_inside_polyhedron(
                top_box_vertices, polyhedron_points_array
            )
            # Draw the other box with the largest angle

            bottom_box_vertices = draw_rectangular_box(
                ax, central_atom_coord, average_split_coord, "purple"
            )

            count_atoms_inside_polyhedron(
                bottom_box_vertices, polyhedron_points_array, is_split=True
            )

            # Now, use
            # Find the average position between the split
            # Find the two largest angles formed
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
    ax, central_atom_coord, large_angle_index_1_coord, color
):
    """
    Step 2. Find the coordinates of the largest angle indices
    """

    # Calculate the line vector
    line_vector = np.array(large_angle_index_1_coord) - np.array(
        central_atom_coord
    )
    norm_value = 3
    # Handling special case where the line vector is vertical or aligned with any axis
    if np.all(line_vector[:2] == 0):  # Line is vertical (change in z only)
        # Choose arbitrary perpendicular vectors in the XY plane
        half_width_vector = np.array(
            [norm_value, 0, 0]
        )  # Arbitrary non-zero length vector along X
        half_height_vector = np.array(
            [0, norm_value, 0]
        )  # Arbitrary non-zero length vector along Y
    else:
        # General case, generate vectors not aligned with the line vector
        if line_vector[0] == 0:
            half_width_vector = np.array([1, 0, 0])
        else:
            half_width_vector = np.array([-line_vector[1], line_vector[0], 0])
        half_width_vector /= np.linalg.norm(half_width_vector)
        half_height_vector = np.cross(line_vector, half_width_vector)
        half_height_vector /= np.linalg.norm(half_height_vector)

    # Scale for visibility
    half_width_vector *= norm_value
    half_height_vector *= norm_value

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
        [central_atom_coord[0], large_angle_index_1_coord[0]],
        [central_atom_coord[1], large_angle_index_1_coord[1]],
        [central_atom_coord[2], large_angle_index_1_coord[2]],
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


def count_atoms_inside_polyhedron(vertices, atom_positions, is_split=False):
    """
    Counts how many atoms are inside the convex polyhedron defined by vertices.
    """
    count = 0
    for i, pos in enumerate(atom_positions):
        if is_inside_convex_polyhedron(pos, vertices):
            count += 1
    if not is_split:
        count_subtracted_central_large_angle = count - 2
    else:
        count_subtracted_central_large_angle = count - 3
    print(
        f"Number of atoms inside the box: {count_subtracted_central_large_angle}"
    )
    return count_subtracted_central_large_angle
