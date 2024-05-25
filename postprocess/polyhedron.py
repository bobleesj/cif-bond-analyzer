import json
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import Delaunay
import numpy as np
from util import folder
import imageio.v3 as iio
import re


def draw_polyhedrons_from_json(
    json_file_path, output_folder, dpi=300
):
    # Load the JSON data
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over each reference label and draw polyhedrons
    for ref_label, connections in data.items():
        ref_coords = set()
        points = []
        for connection in connections:
            ref_coords.add(tuple(connection[2]))
            points.append(connection[2])
            points.append(connection[3])

        # Remove duplicate points
        unique_points = []
        for point in points:
            if point not in unique_points:
                unique_points.append(point)

        # Create a figure for each reference label
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection="3d")
        draw_polyhedron(ax, unique_points, ref_coords, ref_label)

        # Save the figure
        file_path = os.path.join(output_folder, f"{ref_label}.png")
        plt.savefig(file_path, dpi=dpi)
        plt.close(fig)  # Close the figure to free up memory


def draw_incremental_polyhedrons(
    json_file_path, output_folder, dpi=300
):
    # Load the JSON data
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over each reference label and draw incremental polyhedrons
    for ref_label, connections in data.items():
        all_points = []
        min_x, min_y, min_z = float("inf"), float("inf"), float("inf")
        max_x, max_y, max_z = (
            float("-inf"),
            float("-inf"),
            float("-inf"),
        )

        # Collect all points and calculate min/max coordinates for axis scaling
        for connection in connections:
            all_points.extend([connection[2], connection[3]])
            xs, ys, zs = zip(*all_points)
            min_x, max_x = min(min_x, *xs), max(max_x, *xs)
            min_y, max_y = min(min_y, *ys), max(max_y, *ys)
            min_z, max_z = min(min_z, *zs), max(max_z, *zs)

        # List to store unique points and create figures after 4 points
        unique_points = []
        for i, connection in enumerate(connections):
            if connection[2] not in unique_points:
                unique_points.append(connection[2])
            if connection[3] not in unique_points:
                unique_points.append(connection[3])

            # Only plot and save figures after at least 4 unique points
            if len(unique_points) > 4:
                fig = plt.figure(figsize=(8, 6))
                ax = fig.add_subplot(111, projection="3d")

                # Draw the polyhedron with the accumulated points
                draw_polyhedron(
                    ax,
                    unique_points,
                    unique_points,
                    f"{ref_label} - Step {i + 1}",
                )

                # Set consistent axis limits
                ax.set_xlim(min_x, max_x)
                ax.set_ylim(min_y, max_y)
                ax.set_zlim(min_z, max_z)

                # Save the figure
                file_path = os.path.join(
                    output_folder, f"{ref_label}_step_{i + 1}.png"
                )
                plt.savefig(file_path, dpi=dpi)
                plt.close(fig)


def draw_polyhedron(ax, points, ref_coords, label):
    """
    Draw a polyhedron using the provided points.
    """
    if len(points) < 4:
        # Not enough points to form a polyhedron
        return

    # Convert points to numpy array and perform Delaunay triangulation
    points = np.array(points)
    tri = Delaunay(points)
    poly3d = [
        [points[vertex] for vertex in face] for face in tri.simplices
    ]

    # Create a Poly3DCollection object
    poly = Poly3DCollection(poly3d, alpha=0.5, edgecolor="k")
    ax.add_collection3d(poly)

    # Plot the points
    xs, ys, zs = points[:, 0], points[:, 1], points[:, 2]
    ax.scatter(xs, ys, zs, label=label)

    # Highlight the reference atom coordinates
    for ref_coord in ref_coords:
        ax.scatter(*ref_coord, color="r", s=100)  # Larger red points

    # Set labels and title
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(f"Polyhedron for {label}")
    ax.legend()


# Function to extract step number from filename
def get_step_number(filename):
    match = re.search(r"_step_(\d+)", filename)
    return int(match.group(1)) if match else None
