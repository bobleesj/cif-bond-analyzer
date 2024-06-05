import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def plot_polyhedrons(near_180_degrees_atom_indices, CN_connections):
    """
    Plot the best polyhedron for each label using 3D visualization with
    Poly3DCollection.
    """
    color_map = {
        "In1": "blue",
        "U1": "green",
        "Rh1": "yellow",
        "Rh2": "purple",
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
        ax.set_title(f"Best Polyhedron for {label}")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.set_zlabel("Z Coordinate")
        ax.autoscale_view()
        # ax.set_axis_off()  # Hide the axes, as requested

        # Show the plot
        plt.show()
