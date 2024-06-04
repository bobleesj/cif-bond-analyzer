import re
import numpy as np
import matplotlib.tri as mtri
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.ndimage import gaussian_filter
from postprocess.system.figure import ternary


def prepare_data(data_excel, bond_type):
    x, y, z = [], [], []
    for idx, row in data_excel.iterrows():
        formula = row["Formula"]
        value = row[bond_type]
        parts = [float(num) for num in re.findall(r"\d+\.?\d*", formula)]
        total = sum(parts)
        A, B, C = parts
        x_coord = 0.5 * (2 * B + C) / total
        y_coord = (np.sqrt(3) / 2) * C / total
        x.append(x_coord)
        y.append(y_coord)
        z.append(value)
    return x, y, z


def plot_ternary_diagrams(data_excel, bond_types, colors):
    fig, ax = plt.subplots()
    triangulations = []
    # transparency = 0.833
    transparency = 0.833
    contour_smoothing = 20  # lower meaning
    mesh_grid_points = 1000
    # Draw boundary edges
    corners = [(0, 0), (1, 0), (0.5, np.sqrt(3) / 2)]
    ternary.add_vertex_labels(
        corners[0], corners[1], corners[2], ["Er-Er", "Co-Co", "In-In"]
    )
    # Collect all triangulations for a single plot
    for bond_type, color in zip(bond_types, colors):
        # Get all unique formulas

        # Remove the ones with tags

        # For formula:

        # Find the coordinate for formula
        # Get bond fraction per formula
        # For bond fraction:

        """
        Use structural formula for this:
        """

        # It just has to return x, y, z = [], [], [] for each pair
        # Add the edge as fraction

        x, y, z = prepare_data(data_excel, bond_type)
        triangulation = mtri.Triangulation(x, y)
        triangulations.append(triangulation)

        xi, yi = np.meshgrid(
            np.linspace(0, 1, mesh_grid_points),
            np.linspace(0, np.sqrt(3) / 2, mesh_grid_points),
        )
        # interp = mtri.LinearTriInterpolator(triangulation, z)
        interp = mtri.CubicTriInterpolator(triangulation, z, kind="geom")
        zi = interp(xi, yi)

        # Create a custom color map from white to the specified color
        custom_color_map = mcolors.LinearSegmentedColormap.from_list(
            "custom", ["white", color]
        )

        # Plot each set of data on the same axes
        ax.contourf(
            xi,
            yi,
            zi,
            levels=np.linspace(0, 1, contour_smoothing),
            cmap=custom_color_map,
            alpha=1 - transparency,
        )

        # plt.title(f"Ternary Plot for {bond_type}")
        # plt.savefig(f"{bond_type}_ternary_plot.png")  # Save plot as PNG
        # plt.cla()  # Clear the axes for the next plot

        # # Overlay with thicker boundary lines for the triangular grid
        # for triangulation in triangulations:
        #     ax.triplot(
        #         triangulation, "k-", linewidth=1.5
        #     )  # Increased line width for visibility

        ax.plot(
            [corners[0][0], corners[1][0]],
            [corners[0][1], corners[1][1]],
            "k-",
            linewidth=1.5,
        )
        ax.plot(
            [corners[1][0], corners[2][0]],
            [corners[1][1], corners[2][1]],
            "k-",
            linewidth=1.5,
        )
        ax.plot(
            [corners[2][0], corners[0][0]],
            [corners[2][1], corners[0][1]],
            "k-",
            linewidth=1.5,
        )
    ax.set_aspect("equal")  # Ensure the axis are of equal size
    # ax.set_title("Overlay of Ternary Plots with Different Bond Types")
    ax.grid(False)
    ax.figure.savefig(f"color_map_overall-today.png")  # Save plot as PNG
    plt.show()


# Load data
excel_path = "system_analysis_files_binary_ternary.xlsx"
data_excel = pd.read_excel(excel_path)

# Specify bond types and colors
bond_types = [
    "Er-Er-frac",
    "Er-Co-frac",
    "Co-Co-frac",
    "Co-In-frac",
    "In-In-frac",
    "Er-In-frac",
]
colors = [
    "blue",
    "cyan",
    "green",
    "yellow",
    "red",
    "magenta",
]  # Define colors for each bond type

# Plot the overlayed ternary diagrams
plot_ternary_diagrams(data_excel, bond_types, colors)
