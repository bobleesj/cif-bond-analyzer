import numpy as np
import os
from core.util import formula_parser, prompt
import matplotlib.pyplot as plt
from core.system import system_util
from core.system.figure import (
    hexagon,
    ternary,
    binary,
)


def shift_points_xy(point, x_shift, y_shift=0):
    # Shift a point along the x-axis and y-axis
    return np.array([point[0] + x_shift, point[1] + y_shift])


def draw_ternary_figure(
    structure_dict,
    unique_formulas,
    output_dir,
):
    # Config for hexagon
    center_dot_radius = 8
    formula_offset = -0.07
    formula_font_size = 9

    # Grid
    grid_alpha = 0.2
    grid_line_width = 0.5

    # Trinagle frame
    v0, v1, v2 = ternary.generate_traingle_vertex_points()
    ternary.draw_ternary_frame(v0, v1, v2)
    ternary.draw_extra_frame_for_binary_tags(v0, v1, v2, unique_formulas)
    ternary.draw_filled_edges(v0, v1, v2)
    ternary.draw_triangular_grid(
        v0, v1, v2, grid_alpha, grid_line_width, n_lines=10
    )
    legend_center_point = (0, 0.8)
    legend_bond_label_font_size = 10

    # Add legend
    legend_radius = 0.06

    (
        R,
        M,
        X,
    ) = formula_parser.get_RMX_sorted_formula_from_formulas(unique_formulas)
    bond_pair_labels = formula_parser.generate_ordered_bond_labels_from_RMX(
        R, M, X
    )

    """
    Draw legend
    """
    hexagon.draw_single_hexagon_and_lines_per_center_point(
        legend_center_point,
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        radius=legend_radius,
        hex_inner_color="#D3D3D3",
        hex_outer_color="black",
        hex_inner_line_width=0.5,
        hex_outer_line_width=0.5,
        color_line_width=3,
        is_for_individual_hexagon=False,
    )
    plt.scatter(
        legend_center_point[0],
        legend_center_point[1],
        color="black",
        s=14,
        zorder=5,
    )

    # Add legend labels
    label_offset = 0.05

    # Get the points for label positioning using the increased radius
    x_label_pts, y_label_pts = hexagon.get_hexagon_points(
        legend_center_point, legend_radius + label_offset
    )
    for i, (x, y, label) in enumerate(
        zip(x_label_pts, y_label_pts, bond_pair_labels)
    ):
        plt.text(
            x,
            y,
            label,
            fontsize=legend_bond_label_font_size,
            ha="center",  # Horizontal alignment
            va="center",  # Vertical alignment
        )

    """
    Draw legend description
    """
    legend_y_offset = 0.2
    plt.text(
        legend_center_point[0],
        legend_center_point[1] - legend_y_offset,
        "Bar length\nrepresents bond fraction",
        horizontalalignment="center",
        fontsize=8,
    )

    """
    Draw each hexagon point on the traingle.
    """
    # Get orderd R, M, X to find the position of binary compounds
    (
        R_element,
        M_element,
        X_element,
    ) = formula_parser.get_RMX_sorted_formula_from_formulas(unique_formulas)

    # Get all unique formulas
    for formula in unique_formulas:
        (
            bond_fractions_per_formula,
            structures,
        ) = system_util.extract_bond_info_per_formula(formula, structure_dict)

        for i, structure in enumerate(structures):
            formula_formatted = formula_parser.get_subscripted_formula(formula)

            parsed_normalized_formula = formula_parser.get_parsed_norm_formula(
                formula
            )

            num_of_elements = formula_parser.get_num_element(formula)

            center_pt = None

            if num_of_elements == 3:
                R_norm_index = parsed_normalized_formula[0][1]
                M_norm_index = parsed_normalized_formula[1][1]
                R_label = parsed_normalized_formula[0][0]
                M_label = parsed_normalized_formula[1][0]
                X_label = parsed_normalized_formula[2][0]
                labels = [R_label, M_label, X_label]

                center_pt = ternary.get_point_in_triangle_from_ternary_index(
                    v0,
                    v1,
                    v2,
                    float(R_norm_index),
                    float(M_norm_index),
                )

                hexagon.draw_single_hexagon_and_lines_per_center_point(
                    center_pt,
                    bond_fractions_per_formula[i],
                )
                # Add vertex label using ternary formula
                ternary.add_vertex_labels(v0, v1, v2, labels)

            # For binary
            if num_of_elements == 2:
                # 6 cases,
                """
                RM(AB) are RM
                RX(AC)
                """

                tag = formula_parser.extract_tag(formula)
                # Now, if the formula contains any of the tags, then we alter

                A_norm_index = float(parsed_normalized_formula[0][1])
                B_norm_index = float(parsed_normalized_formula[1][1])
                A_label = parsed_normalized_formula[0][0]
                B_label = parsed_normalized_formula[1][0]
                labels = [A_label, B_label]

                if A_label == R_element and B_label == M_element:
                    # ErCo
                    center_pt = (
                        ternary.get_point_in_triangle_from_ternary_index(
                            v0,
                            v1,
                            v2,
                            A_norm_index,
                            B_norm_index,
                        )
                    )
                    if tag == "hex":
                        center_pt = center_pt
                    elif tag == "lt":
                        center_pt = shift_points_xy(center_pt, 0.0, -0.1)
                    elif tag == "ht":
                        center_pt = shift_points_xy(center_pt, 0.0, -0.2)
                    elif tag is not None:
                        center_pt = shift_points_xy(center_pt, 0.0, -0.1)

                    hexagon.draw_single_hexagon_and_lines_per_center_point(
                        center_pt,
                        bond_fractions_per_formula[i],
                    )
                if A_label == R_element and B_label == X_element:
                    center_pt = (
                        ternary.get_point_in_triangle_from_ternary_index(
                            v0,
                            v1,
                            v2,
                            A_norm_index,
                            0.0,
                        )
                    )
                    if tag == "hex":
                        center_pt = center_pt
                    elif tag == "lt":
                        center_pt = shift_points_xy(center_pt, -0.1, 0.0)
                    elif tag == "ht":
                        center_pt = shift_points_xy(center_pt, -0.2, 0.0)
                    elif tag is not None:
                        center_pt = shift_points_xy(center_pt, -0.1, 0.0)

                    hexagon.draw_single_hexagon_and_lines_per_center_point(
                        center_pt,
                        bond_fractions_per_formula[i],
                    )
                if A_label == M_element and B_label == X_element:
                    # CoIn2
                    center_pt = (
                        ternary.get_point_in_triangle_from_ternary_index(
                            v0,
                            v1,
                            v2,
                            0,
                            (1 - B_norm_index),
                        )
                    )
                    if tag == "hex":
                        center_pt = center_pt
                    elif tag == "lt":
                        center_pt = shift_points_xy(center_pt, 0.1, 0.0)
                    elif tag == "ht":
                        center_pt = shift_points_xy(center_pt, 0.2, 0.0)
                    elif tag is not None:
                        center_pt = shift_points_xy(center_pt, 0.1, 0.0)

                    hexagon.draw_single_hexagon_and_lines_per_center_point(
                        center_pt,
                        bond_fractions_per_formula[i],
                    )
            # Write one of the chemical formulas
            plt.text(
                center_pt[0],
                center_pt[1] + formula_offset,
                f"{formula_formatted}",
                fontsize=formula_font_size,
                ha="center",
            )

            # Add the "center dot" in each hexagon
            plt.scatter(
                center_pt[0],
                center_pt[1],
                color="black",
                s=center_dot_radius,
                zorder=6,
            )

    output_filepath = os.path.join(output_dir, "ternary.png")
    plt.axis("off")
    plt.savefig(output_filepath, dpi=300)
    plt.close()


def draw_hexagon_for_individual_figure(
    structure_dict,
    unique_structure_types,
    output_dir,
):
    hexagon_image_files = []
    center_pt = (0, 0)

    # Individual hexagon (modified)
    radius = 1
    radius_padding = 0.3
    bond_label_font_size = 16
    outer_line_width = 2
    color_line_width = 6
    inner_line_width = 1
    core_dot_radius = 55

    # Formula/structure label
    label_offset = 0.5
    formula_font_size = 15
    formula_offset = -2.5

    individuals_dir = os.path.join(output_dir, "individuals")
    os.makedirs(
        individuals_dir, exist_ok=True
    )  # Create the directory if it doesn't exist

    for _, structure in enumerate(unique_structure_types):
        result = system_util.extract_info_per_structure(
            structure_dict, structure
        )
        formulas, bond_labels, bond_fractions = result
        formula = formula_parser.get_subscripted_formula(formulas[0])
        structure = formula_parser.get_subscripted_formula(structure)

        fig, ax = plt.subplots(figsize=(3, 3.5), dpi=300)
        plt.subplots_adjust(top=1.1)

        hexagon.draw_single_hexagon_and_lines_per_center_point(
            center_pt,
            bond_fractions,
            radius=radius,
            hex_inner_color="#D3D3D3",
            hex_outer_color="black",
            hex_inner_line_width=inner_line_width,
            hex_outer_line_width=outer_line_width,
            color_line_width=color_line_width,
            is_for_individual_hexagon=True,
        )

        plt.scatter(0, 0, color="black", s=core_dot_radius, zorder=5)

        # Add formula/structure names
        plt.text(
            center_pt[0],
            center_pt[1] + formula_offset,
            f"Formula: {formula}\nStructure: {structure}",
            fontsize=formula_font_size,
            ha="center",
        )

        label_radius = radius + label_offset

        # Get the points for label positioning using the increased radius
        x_label_pts, y_label_pts = hexagon.get_hexagon_points(
            center_pt, label_radius
        )

        # Find minimum and maximum for both x and y from the hexagon points
        x_min, x_max = min(x_label_pts), max(x_label_pts)
        y_min, y_max = min(y_label_pts), max(y_label_pts)

        ax.set_xlim(x_min - radius_padding, x_max + radius_padding)
        ax.set_ylim(y_min - radius_padding, y_max + radius_padding)

        for i, (x, y, label) in enumerate(
            zip(x_label_pts, y_label_pts, bond_labels)
        ):
            plt.text(
                x,
                y,
                label,
                fontsize=bond_label_font_size,  # Adjust fontsize as needed
                ha="center",  # Horizontal alignment
                va="center",  # Vertical alignment
            )

        ax.set_aspect("equal", adjustable="box")
        ax.axis("off")

        # Saving each hexagon to a file
        hexagon_filename = f"{formulas[0]}.png"
        hexagon_filepath = os.path.join(individuals_dir, hexagon_filename)
        fig.savefig(hexagon_filepath, dpi=300)
        plt.close(fig)
        hexagon_image_files.append(hexagon_filepath)

    """
    Save composite figures files
    """
    # Constants for the layout
    max_images_per_figure = 12
    rows_per_figure = 4
    cols_per_figure = 3

    # Calculate the number of figures needed
    num_figures = int(
        np.ceil(len(hexagon_image_files) / max_images_per_figure)
    )

    for fig_idx in range(num_figures):
        # Calculate the range of images for this figure
        start_idx = fig_idx * max_images_per_figure
        end_idx = min(
            (fig_idx + 1) * max_images_per_figure,
            len(hexagon_image_files),
        )
        current_images = hexagon_image_files[start_idx:end_idx]

        # Create figure and axes
        fig, axs = plt.subplots(
            nrows=rows_per_figure,
            ncols=cols_per_figure,
            figsize=(5, 8),
        )
        axs = axs.flatten()

        # Plot each image in the current set
        for ax, hexagon_image in zip(axs, current_images):
            img = plt.imread(hexagon_image)
            ax.imshow(img)
            ax.axis("off")

        # Remove unused axes
        for ax in axs[len(current_images) :]:
            ax.remove()

        # Adjust layout
        plt.subplots_adjust(
            left=0.1,
            right=0.9,
            top=0.85,
            bottom=0.15,
            wspace=0.2,
            hspace=0.0,
        )

        # Save this figure
        composite_filepath = os.path.join(
            output_dir, f"composite_{fig_idx+1}.png"
        )
        fig.savefig(composite_filepath, dpi=300)
        plt.close(fig)
        print(f"Saved composite hexagon image {fig_idx+1} in {output_dir}")


def draw_binary_figure(
    formulas,
    structure_dict,
    possible_bond_pairs,
    output_dir,
    is_single_binary,
):
    # Handle binaries with various bond types
    for bond_pair in possible_bond_pairs:
        bond_pair_set = set(bond_pair)
        counter = 0
        for formula in formulas:
            # Parse the formula and check whether it is in the bond_pair
            parsed_elements = set(formula_parser.get_unique_elements(formula))
            if parsed_elements == bond_pair_set:
                (
                    bond_fractions_per_formula,
                    structures,
                ) = system_util.extract_bond_info_per_formula(
                    formula, structure_dict
                )

                binary.draw_horizontal_lines_with_multiple_marks(
                    formula,
                    bond_fractions_per_formula,
                    structures,
                    is_single_binary,
                )
                counter += 1

        # Save the figure for each bond pair
        if counter != 0:
            output_filename = (
                "binnary_" + bond_pair[0] + "-" + bond_pair[1] + ".png"
            )
            output_filepath = os.path.join(output_dir, output_filename)
            plt.savefig(output_filepath, dpi=300)
            plt.close()
