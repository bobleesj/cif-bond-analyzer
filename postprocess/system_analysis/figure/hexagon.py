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


def draw_single_hexagon_and_lines_per_center_point(
    center_pt,
    bond_fractions,
    is_binary,
    is_for_individual_hexagon,
    radius=0.05,
    hex_inner_color="#D3D3D3",
    hex_outer_color="#D3D3D3",
    hex_inner_line_width=0.5,
    hex_outer_line_width=0.5,
    color_line_width=2.5,
):
    # Get colors
    colors = color.get_hexagon_vertex_colors(False)
    # Get hexagon poitns
    x_hex_pts, y_hex_pts = hexagon.get_hexagon_points(
        center_pt, radius
    )

    if is_for_individual_hexagon:
        black_line_width = color_line_width + 2.5
    else:
        black_line_width = color_line_width + 1

    draw_hexagon_outline(
        x_hex_pts,
        y_hex_pts,
        hex_outer_line_width,
        hex_outer_color,
    )

    draw_hexagon_center_to_vertex(
        center_pt,
        x_hex_pts,
        y_hex_pts,
        hex_inner_line_width,
        hex_inner_color,
    )

    draw_colored_and_black_lines(
        x_hex_pts,
        y_hex_pts,
        center_pt,
        bond_fractions,
        colors,
        color_line_width,
        black_line_width,
        is_for_individual_hexagon,
    )


def draw_hexagon_outline(x_hex_pts, y_hex_pts, lw, color):
    # Draw hexagon outline
    plt.plot(x_hex_pts, y_hex_pts, "-", lw=lw, color=color, zorder=3)


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
    x_hex_pts,
    y_hex_pts,
    center_pt,
    bond_fractions,
    colors,
    color_line_width,
    black_line_width,
    is_for_individual_hexagon,
):
    num_of_point = 6
    # print("let draw single hexagon")
    # print(bond_fractions)
    # print(np.round(center_pt, 3))

    for i in range(num_of_point):
        x_hex_pt = x_hex_pts[i]
        y_hex_pt = y_hex_pts[i]
        bond_fraction = bond_fractions[i]
        x_color_pt, y_color_pt = get_norm_positions(
            x_hex_pt, y_hex_pt, center_pt, bond_fraction
        )

        plot_colored_black_lines_with_fraction(
            center_pt,
            x_hex_pt,
            y_hex_pt,
            x_color_pt,
            y_color_pt,
            color_line_width,
            black_line_width,
            colors[i],
            is_for_individual_hexagon,
        )


def get_norm_positions(x, y, center_pt, bond_fraction):
    norm_x = center_pt[0] + bond_fraction * (x - center_pt[0])
    norm_y = center_pt[1] + bond_fraction * (y - center_pt[1])
    return norm_x, norm_y


def plot_colored_black_lines_with_fraction(
    center_pt,
    x_hex_pt,
    y_hex_pt,
    x_color_pt,
    y_color_pt,
    lw,
    black_lw,
    color,
    is_for_individual_hexagon,
):
    if is_for_individual_hexagon:
        order = 5
        scale = 0.018
        # Calculate the unit vector for the color point
        dx = x_color_pt - center_pt[0]
        dy = y_color_pt - center_pt[1]
        dist = np.sqrt(dx**2 + dy**2)
        unit_vector = np.array([dx, dy]) / dist

        # Calculate the unit vector for the hexagon vertex
        dx_hex = x_hex_pt - center_pt[0]
        dy_hex = (
            y_hex_pt - center_pt[1]
        )  # Corrected from center_pt[0] to center_pt[1]
        dist_hex = np.sqrt(dx_hex**2 + dy_hex**2)
        hex_unit_vector = np.array([dx_hex, dy_hex]) / dist_hex

        # Adjust endpoint by half the marker radius
        marker_adjustment = lw * scale
        start_offset = marker_adjustment / 2  # Half the marker size
        start_color_x = (
            center_pt[0] + hex_unit_vector[0] * start_offset
        )
        start_color_y = (
            center_pt[1] + hex_unit_vector[1] * start_offset
        )

        end_color_x = center_pt[0] + unit_vector[0] * (
            dist - start_offset
        )
        end_color_y = center_pt[1] + unit_vector[1] * (
            dist - start_offset
        )

        # Draw the colored line
        plt.plot(
            [start_color_x, end_color_x],
            [start_color_y, end_color_y],
            "-",
            lw=lw,
            color=color,
            zorder=order,
        )
        # Black line
        plt.plot(
            [start_color_x, end_color_x],
            [start_color_y, end_color_y],
            "-",
            lw=black_lw,
            color="black",
            zorder=order - 1,
        )
    if not is_for_individual_hexagon:
        order = 5
        scale = 0.003
        # Calculate the unit vector for the color point
        dx = x_color_pt - center_pt[0]
        dy = y_color_pt - center_pt[1]
        dist = np.sqrt(dx**2 + dy**2)
        unit_vector = np.array([dx, dy]) / dist

        # Calculate the unit vector for the hexagon vertex
        dx_hex = x_hex_pt - center_pt[0]
        dy_hex = (
            y_hex_pt - center_pt[1]
        )  # Corrected from center_pt[0] to center_pt[1]
        dist_hex = np.sqrt(dx_hex**2 + dy_hex**2)
        hex_unit_vector = np.array([dx_hex, dy_hex]) / dist_hex

        # Adjust endpoint by half the marker radius
        marker_adjustment = lw * scale
        start_offset = marker_adjustment / 2  # Half the marker size
        start_color_x = (
            center_pt[0] + hex_unit_vector[0] * start_offset
        )
        start_color_y = (
            center_pt[1] + hex_unit_vector[1] * start_offset
        )

        end_color_x = center_pt[0] + unit_vector[0] * (
            dist - start_offset
        )
        end_color_y = center_pt[1] + unit_vector[1] * (
            dist - start_offset
        )

        # Draw the colored line
        plt.plot(
            [start_color_x, end_color_x],
            [start_color_y, end_color_y],
            "-",
            lw=lw,
            color=color,
            zorder=order,
        )
        # Black line
        plt.plot(
            [start_color_x, end_color_x],
            [start_color_y, end_color_y],
            "-",
            lw=black_lw,
            color="black",
            zorder=order - 1,
        )
