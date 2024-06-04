import re
import numpy as np
from os.path import join
import matplotlib.tri as mtri
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

from postprocess.system.figure import ternary
from util import formula_parser
from postprocess.system.figure.color import get_hexagon_vertex_colors
from postprocess.system import system_util


def plot_ternary_color_map(unique_formulas, structure_dict, output_dir):
    # Plot the overlayed ternary diagrams
    fig, ax = plt.subplots()
    triangulations = []
    transparency = 0.8333
    contour_smoothing = 10
    mesh_grid_points = 1000

    # Draw boundary edges
    (R, M, X) = formula_parser.get_RMX_sorted_formula_from_formulas(
        unique_formulas
    )
    corners = [(0, 0), (1, 0), (0.5, np.sqrt(3) / 2)]
    ternary.add_vertex_labels(
        corners[0],
        corners[1],
        corners[2],
        [
            f"{R}-{R}",
            f"{M}-{M}",
            f"{X}-{X}",
        ],
    )
    # Color 6 colors for ternary
    colors = get_hexagon_vertex_colors(False)

    for i, color in enumerate(colors):
        formulas = []
        x_all_per_bond_type = []
        y_all_per_bond_type = []
        z_all_per_bond_type = []
        # Loop through each formula
        for formula in unique_formulas:
            (
                bond_fractions,
                _,
            ) = system_util.extract_bond_info_per_formula(
                formula, structure_dict
            )

            # Skip formulas with tags (assuming extract_tag function is defined in formula_parser)
            tag = formula_parser.extract_tag(formula)
            if tag:
                continue

            bond_fractions_first_structure = bond_fractions[0]
            (
                A_norm_comp,
                B_norm_comp,
                C_norm_comp,
            ) = formula_parser.get_composition_from_binary_ternary(
                formula, (R, M, X)
            )
            # Calculate coordinates based on the normalized composition
            total = A_norm_comp + B_norm_comp + C_norm_comp
            x_coord = 0.5 * (2 * B_norm_comp + C_norm_comp) / total
            y_coord = (np.sqrt(3) / 2) * C_norm_comp / total
            x_all_per_bond_type.append(x_coord)
            y_all_per_bond_type.append(y_coord)
            z_all_per_bond_type.append(bond_fractions_first_structure[i])
            formulas.append(formula)

            """
            If it is Er-Er (i=0) or Co-Co (i=2) or In-In (i=4), include (1,0,0), (0,1,0), (0,0,1)
            since the vertices have a single bond type only.
            """

            if i == 0:
                x_all_per_bond_type.append(0)
                y_all_per_bond_type.append(0)
                z_all_per_bond_type.append(1.0)
            if i == 2:
                x_all_per_bond_type.append(1)
                y_all_per_bond_type.append(0)
                z_all_per_bond_type.append(1.0)
            if i == 4:
                x_all_per_bond_type.append(0.5)
                y_all_per_bond_type.append(np.sqrt(3) / 2)
                z_all_per_bond_type.append(1.0)

        """
        It is odd that CoIn3 has 3 different structures
        All bond fractions are same regardless.
        # bond fraction:
        # [[0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
        # [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
        # [0.0, 0.0, 0.0, 1.0, 0.0, 0.0]]
        # structures found: ['IrIn3', 'RuIn3', 'U3Si2']
        # """

        triangulation = mtri.Triangulation(
            x_all_per_bond_type, y_all_per_bond_type
        )
        triangulations.append(triangulation)

        xi, yi = np.meshgrid(
            np.linspace(0, 1, mesh_grid_points),
            np.linspace(0, np.sqrt(3) / 2, mesh_grid_points),
        )
        # interp = mtri.LinearTriInterpolator(triangulation, z)
        interp = mtri.CubicTriInterpolator(
            triangulation, z_all_per_bond_type, kind="geom"
        )
        zi = interp(xi, yi)

        # Create a custom color map from white to the specified color
        custom_color_map = mcolors.LinearSegmentedColormap.from_list(
            "custom", ["white", color]
        )

        ax.contourf(
            xi,
            yi,
            zi,
            levels=np.linspace(0, 1, contour_smoothing),
            cmap=custom_color_map,
            alpha=1 - transparency,
        )

        # plt.title(f"Ternary Plot for {color}")

        # plt.savefig(
        #     join(output_dir, f"color_map_{color}.png")
        # )  # Save plot as PNG
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
    ax.grid(False)
    ax.set_axis_off()
    ax.set_aspect("equal")  # Ensure the axis are of equal size
    # ax.set_title("Overlay of Ternary Plots with Different Bond Types")
    ax.figure.savefig(join(output_dir, f"color_map_overall-today.png"))
    plt.show()