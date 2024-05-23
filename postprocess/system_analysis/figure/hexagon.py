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
    radius=0.05,
    hex_outline_color="#D3D3D3",
    hex_inner_line_width=0.5,
    hex_outer_line_width=0.5,
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

    if is_individual_hexagonal:
        black_line_width = color_line_width + 2
    else:
        black_line_width = color_line_width + 1

    draw_hexagon_outline(
        center_pt,
        x_hex_pts,
        y_hex_pts,
        hex_outer_line_width,
        hex_outline_color,
    )

    draw_hexagon_center_to_vertex(
        center_pt,
        x_hex_pts,
        y_hex_pts,
        hex_inner_line_width,
        hex_outline_color,
    )

    draw_colored_and_black_lines(
        is_binary,
        x_hex_pts,
        y_hex_pts,
        center_pt,
        bond_fractions,
        colors,
        color_line_width,
        black_line_width,
    )


def draw_hexagon_outline(center_pt, x_hex_pts, y_hex_pts, lw, color):
    # Draw hexagon outline
    plt.plot(
        x_hex_pts,
        y_hex_pts,
        "-",
        lw=lw,
        color=color,
    )


def draw_hexagon_center_to_vertex(
    center_pt, x_hex_pts, y_hex_pts, lw, color
):
    # Draw center to vertices
    for x, y in zip(x_hex_pts, y_hex_pts):
        plt.plot(
            [center_pt[0], x],
            [center_pt[1], y],
            "-",
            lw=lw,
            color=color,
        )


def draw_colored_and_black_lines(
    is_binary,
    x_hex_pts,
    y_hex_pts,
    center_pt,
    bond_fractions,
    colors,
    color_line_width,
    black_line_width,
):
    if is_binary:
        num_points = 3
        for i in range(num_points):
            x = x_hex_pts[i]
            y = y_hex_pts[i]
            bond_fraction = bond_fractions[i]
            norm_x, norm_y = get_norm_positions(
                x, y, center_pt, bond_fraction
            )
            plot_colored_black_lines_with_fraction(
                center_pt,
                norm_x,
                norm_y,
                color_line_width,
                colors[i],
            )

    if not is_binary:
        # Draw colored lins
        for i, (x, y) in enumerate(
            zip(x_hex_pts[:-1], y_hex_pts[:-1])
        ):  # Exclude the last repeated point
            bond_fraction = bond_fractions[i]
            norm_x, norm_y = get_norm_positions(
                x, y, center_pt, bond_fraction
            )

            plot_colored_black_lines_with_fraction(
                center_pt,
                norm_x,
                norm_y,
                color_line_width,
                colors[i],
            )


def get_norm_positions(x, y, center_pt, bond_fraction):
    norm_x = center_pt[0] + bond_fraction * (x - center_pt[0])
    norm_y = center_pt[1] + bond_fraction * (y - center_pt[1])
    return norm_x, norm_y


def plot_colored_black_lines_with_fraction(
    center_pt, x, y, lw, color
):
    order = 3
    # Calculate the distance between the points
    dx = x - center_pt[0]
    dy = y - center_pt[1]
    dist = np.sqrt(dx**2 + dy**2)

    # Calculate the marker radius in data units
    # Assuming the figure dpi is standard (could vary),
    # and the axes are scaled equally
    fig_dpi = plt.gcf().dpi
    marker_radius_in_pixels = np.sqrt(lw)
    marker_radius_in_data_units = (
        marker_radius_in_pixels
        * (dist / np.sqrt(dx**2 + dy**2))
        / fig_dpi
    )

    # Calculate the new endpoint that subtracts the marker radius
    new_x = x - (marker_radius_in_data_units / dist) * dx
    new_y = y - (marker_radius_in_data_units / dist) * dy

    # Draw the line to the new endpoint
    plt.plot(
        [center_pt[0], new_x],
        [center_pt[1], new_y],
        "-",
        lw=lw,
        color=color,
        zorder=order,
    )

    # Black lines underneath the colored lines
    plt.plot(
        [center_pt[0], new_x],
        [center_pt[1], new_y],
        "-",
        lw=lw + 1,
        color="black",
        zorder=order - 1,
    )
