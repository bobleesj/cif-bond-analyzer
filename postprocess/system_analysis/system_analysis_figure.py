import numpy as np
from os.path import join
from util import formula_parser, prompt
import matplotlib.pyplot as plt
from postprocess.system_analysis import system_analysis
from postprocess.system_analysis.figure import (
    hexagon,
    ternary,
    binary,
)


def draw_ternary_figure(
    structure_dict,
    unique_structure_types,
    unique_formulas,
    output_dir,
    is_binary_ternary_combined,
):
    if is_binary_ternary_combined:
        print("let's draw a ternary diagram combining ternary/binary")

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
    ternary.draw_filled_edges(v0, v1, v2)
    ternary.draw_triangular_grid(
        v0, v1, v2, grid_alpha, grid_line_width, n_lines=10
    )

    # Get all unique formulas
    for formula in unique_formulas:
        (
            bond_fractions_per_formula,
            structures,
        ) = system_analysis.extract_bond_info_per_formula(
            formula, structure_dict
        )

        for i, structure in enumerate(structures):
            formula_formatted = (
                formula_parser.get_subscripted_formula(formula)
            )

            parsed_normalized_formula = (
                formula_parser.get_parsed_norm_formula(formula)
            )

            num_of_elements = formula_parser.get_num_element(formula)

            center_pt = None
            is_for_individual_hexagon = False

            if num_of_elements == 3:
                R_norm_index = parsed_normalized_formula[0][1]
                M_norm_index = parsed_normalized_formula[1][1]
                R_label = parsed_normalized_formula[0][0]
                M_label = parsed_normalized_formula[1][0]
                X_label = parsed_normalized_formula[2][0]
                labels = [R_label, M_label, X_label]

                center_pt = (
                    ternary.get_point_in_triangle_from_ternary_index(
                        v0,
                        v1,
                        v2,
                        float(R_norm_index),
                        float(M_norm_index),
                    )
                )
                hexagon.draw_single_hexagon_and_lines_per_center_point(
                    center_pt,
                    bond_fractions_per_formula[i],
                    False,
                    is_for_individual_hexagon,
                )
                # Add vertex label using ternary formula
                ternary.add_vertex_labels(v0, v1, v2, labels)

            # For binary
            if num_of_elements == 2:
                A_norm_index = parsed_normalized_formula[0][1]
                B_norm_index = parsed_normalized_formula[1][1]
                A_label = parsed_normalized_formula[0][0]
                B_label = parsed_normalized_formula[1][0]
                labels = [A_label, B_label]

                center_pt = (
                    ternary.get_point_in_triangle_from_ternary_index(
                        v0,
                        v1,
                        v2,
                        float(0),
                        (1 - float(B_norm_index)),
                    )
                )

                hexagon.draw_single_hexagon_and_lines_per_center_point(
                    center_pt,
                    bond_fractions_per_formula[i],
                    True,
                    is_for_individual_hexagon,
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

    output_filepath = join(output_dir, "ternary.png")
    plt.savefig(output_filepath, dpi=300)
    plt.close()


def draw_hexagon_for_individual_figure(
    structure_dict,
    unique_structure_types,
    output_dir,
    is_binary,
    is_individual_hexagonal,
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
    core_dot_radius = 50

    # Formula/structure label
    label_offset = 0.5
    formula_font_size = 15
    formula_offset = -2.5
    for _, structure in enumerate(unique_structure_types):
        result = system_analysis.extract_info_per_structure(
            structure_dict, structure
        )
        formulas, bond_labels, bond_fractions = result
        formula = formula_parser.get_subscripted_formula(formulas[0])
        structure = formula_parser.get_subscripted_formula(structure)

        fig, ax = plt.subplots(figsize=(3, 3.5), dpi=300)
        plt.subplots_adjust(
            top=1.1
        )  # Adjust this value to reduce the space at the top

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
            is_binary=is_binary,
        )

        plt.scatter(0, 0, color="black", s=core_dot_radius, zorder=5)

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
        hexagon_filepath = join(output_dir, hexagon_filename)
        fig.savefig(hexagon_filepath, dpi=300)
        plt.close(fig)
        hexagon_image_files.append(hexagon_filepath)

    # Generate a composite image of all hexagons
    fig, axs = plt.subplots(
        nrows=int(np.ceil(len(hexagon_image_files) / 3)),
        ncols=3,
        figsize=(5, 8),
    )
    axs = axs.flatten()

    for ax, hexagon_image in zip(axs, hexagon_image_files):
        img = plt.imread(hexagon_image)
        ax.imshow(img)
        ax.axis("off")

    # Remove empty subplots
    for ax in axs[len(hexagon_image_files) :]:
        ax.remove()

    # Give padding for each subplot
    plt.subplots_adjust(
        left=0.1,
        right=0.9,
        top=0.85,
        bottom=0.15,
        wspace=0.2,  # Space between subplots, horizontally
        hspace=0.0,  # Space between subplots, vertically
    )

    # Save the composite sheet
    composite_filepath = join(output_dir, "composite_hexagons.png")
    fig.savefig(composite_filepath, dpi=300)

    plt.close(fig)

    print(
        f"Saved individual hexagon images and a composite in {output_dir}"
    )


def draw_binary_figure(structure_dict, output_dir):
    bond_count_dict = system_analysis.extract_bond_counts(
        structure_dict
    )
    norm_bond_count_dict = system_analysis.normalize_bond_counts(
        bond_count_dict
    )
    prompt.print_dict_in_json(norm_bond_count_dict)

    binary.draw_horizontal_lines_with_multiple_marks(
        norm_bond_count_dict
    )

    plt.show()
    plt.close()
