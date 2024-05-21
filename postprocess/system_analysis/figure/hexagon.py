import random
import numpy as np
import matplotlib.pyplot as plt
from postprocess.system_analysis.figure import hexagon, color


def get_hexagon_points(center, size):
    """Generate points for a hexagon rotated to stand on a vertex."""
    angles = np.linspace(0, 2 * np.pi, 7, endpoint=True) + 7 * (
        np.pi / 6
    )  # Rotate by 30 degrees
    x_hex = center[0] + size * np.cos(angles)
    y_hex = center[1] + size * np.sin(angles)
    return np.around(x_hex, 3), np.around(y_hex, 3)


def draw_hexagon_per_center_point(
    center_pt, bond_fractions, radius=0.04
):
    alpha_value = 0.3
    color_line_width = 2.5
    radius = 0.05

    x_hex_pts, y_hex_pts = hexagon.get_hexagon_points(
        center_pt, radius
    )

    # Draw outline
    plt.plot(
        x_hex_pts,
        y_hex_pts,
        "-",
        lw=0.5,
        alpha=alpha_value,
        color="black",
    )

    # Draw center to vertices
    for x, y in zip(x_hex_pts, y_hex_pts):
        plt.plot(
            [center_pt[0], x],
            [center_pt[1], y],
            "k",
            alpha=alpha_value,
            lw=0.3,
        )

    colors = color.get_hexagon_vertex_colors()

    # Draw colored lins
    for i, (x, y) in enumerate(
        zip(x_hex_pts[:-1], y_hex_pts[:-1])
    ):  # Exclude the last repeated point
        bond_fraction = bond_fractions[i]
        norm_x = center_pt[0] + bond_fraction * (x - center_pt[0])
        norm_y = center_pt[1] + bond_fraction * (y - center_pt[1])
        plt.plot(
            [center_pt[0], norm_x],
            [center_pt[1], norm_y],
            "-",
            lw=color_line_width,
            color=colors[i],
        )
