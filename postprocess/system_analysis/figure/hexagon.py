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
    is_binary=False,
):
    # Get colors
    colors = color.get_hexagon_vertex_colors(is_binary)

    # Get hexagon poitns
    x_hex_pts, y_hex_pts = hexagon.get_hexagon_points(
        center_pt, radius
    )

    # Draw hexagon outline
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

    # Use only the first 3 values of bond fractions
    if is_binary:
        # Use only the first 3 values of bond fractions and hex points
        num_points = (
            3  # Only use the first three points for a binary compound
        )
        for i in range(num_points):
            x = x_hex_pts[i]
            y = y_hex_pts[i]
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

    # # Use only the first 6 values of bond fractions
    if not is_binary:
        # Draw colored lins
        for i, (x, y) in enumerate(
            zip(x_hex_pts[:-1], y_hex_pts[:-1])
        ):  # Exclude the last repeated point
            bond_fraction = bond_fractions[i]
            norm_x = center_pt[0] + bond_fraction * (x - center_pt[0])
            norm_y = center_pt[1] + bond_fraction * (y - center_pt[1])

            # Draw black underneath color
            plt.plot(
                [center_pt[0], norm_x],
                [center_pt[1], norm_y],
                "-",
                lw=color_line_width + 2,
                color="black",
                zorder=2,
                alpha=1,
            )

            plt.plot(
                [center_pt[0], norm_x],
                [center_pt[1], norm_y],
                "-",
                lw=color_line_width,
                color=colors[i],
                zorder=3,
            )

            start_offset = 0.01  # Distance to start from the actual endpoint, adjust as needed
            outward_length = 0.01  # Adjust this value as needed

            # Calculate the direction of the original line from the center to the endpoint and normalize
            direction = np.array([norm_x, norm_y])
            direction_norm = direction / np.linalg.norm(direction)

            # Extend the endpoint outward along the same direction
            start_offset = 0.01  # Distance to start from the actual endpoint, adjust as needed
            outward_length = 0.01  # Adjust this value as needed

            #     # Calculate the direction of the original line from the center to the endpoint and normalize

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
            # plt.plot(
            #     [start_point[0], extended_point[0]],  # x
            #     [start_point[1], extended_point[1]],  # y
            #     "-",
            #     lw=color_line_width,
            #     color="black",
            #     zorder=4,
            # )
