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

    return np.around(x_hex, 5), np.around(y_hex, 5)


def draw_hexagon_per_center_point(
    center_pt,
    bond_fractions,
    radius=0.04,
    inner_alpha=0.3,
    outer_alpha=0.3,
    inner_line_width=0.5,
    outer_line_width=0.5,
    color_line_width=2.5,
    is_individual_hexagonal=False,
):
    x_hex_pts, y_hex_pts = hexagon.get_hexagon_points(
        center_pt, radius
    )

    # Draw outline
    plt.plot(
        x_hex_pts,
        y_hex_pts,
        "-",
        lw=outer_line_width,
        alpha=outer_alpha,
        color="black",
    )

    # Draw center to vertices
    for x, y in zip(x_hex_pts, y_hex_pts):
        plt.plot(
            [center_pt[0], x],
            [center_pt[1], y],
            "k",
            alpha=inner_alpha,
            lw=inner_line_width,
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
            zorder=3,
        )

        if is_individual_hexagonal:
            start_offset = 0.05  # Distance to start from the actual endpoint, adjust as needed
            outward_length = 0.01  # Adjust this value as needed

            # Calculate the direction of the original line from the center to the endpoint and normalize
            direction = np.array([norm_x, norm_y])
            direction_norm = direction / np.linalg.norm(direction)

            # Start the black line slightly away from the endpoint
            start_point = (
                np.array([norm_x, norm_y])
                + direction_norm * start_offset
            )

            # Extend the endpoint outward along the same direction
            extended_point = np.array(
                [norm_x, norm_y]
            ) + direction_norm * (outward_length + start_offset)

            # Draw the line from the start point to the extended point
            plt.plot(
                [start_point[0], extended_point[0]],  # x
                [start_point[1], extended_point[1]],  # y
                "-",
                lw=color_line_width,
                # lw=2,
                color="black",
            )
