import random
import numpy as np
import os
from os.path import join
from util import formula_parser, sort, folder, prompt
import matplotlib.pyplot as plt
from postprocess.system_analysis import system_analysis
from postprocess.system_analysis.figure import (
    hexagon,
    ternary,
    binary,
)


def draw_ternary_figure(
    structure_dict, unique_structure_types, output_dir
):
    formula_offset = -0.07
    formula_font_size = 9
    v0, v1, v2 = ternary.generate_traingle_vertex_points()
    ternary.draw_ternary_frame(v0, v1, v2)
    ternary.draw_filled_edges(v0, v1, v2)

    for structure in unique_structure_types:
        result = system_analysis.extract_structure_info(
            structure_dict, structure
        )
        formulas, _, bond_fractions = result
        formula = formulas[0]
        formula_formatted = formula_parser.get_subscripted_formula(
            formula
        )

        parsed_normalized_formula = (
            formula_parser.get_parsed_norm_formula(formula)
        )

        # Sort the formula based on Mendeeleeve
        R_norm_index = parsed_normalized_formula[0][1]
        M_norm_index = parsed_normalized_formula[1][1]
        R_label = parsed_normalized_formula[0][0]
        M_label = parsed_normalized_formula[1][0]
        X_label = parsed_normalized_formula[2][0]
        labels = [R_label, M_label, X_label]

        center_point = ternary.get_point_in_triangle_from_norm_index(
            v0, v1, v2, float(R_norm_index), float(M_norm_index)
        )
        hexagon.draw_hexagon_per_center_point(
            center_point, bond_fractions, 0.05
        )
        # Write one of the chemical formulas
        plt.text(
            center_point[0],
            center_point[1] + formula_offset,
            formula_formatted,
            fontsize=formula_font_size,
            ha="center",
        )
        plt.scatter(
            center_point[0],
            center_point[1],
            color="black",
            s=1,
            zorder=3,
        )

    ternary.add_vertex_labels(v0, v1, v2, labels)
    output_filepath = join(output_dir, "ternary.png")
    plt.savefig(output_filepath, dpi=300)
    plt.close()


def draw_individual_hexagon(
    structure_dict,
    unique_structure_types,
    output_dir,
    is_individual_hexagonal=False,
):
    hexagon_image_files = []
    center_pt = (0, 0)

    # Individual hexagon
    radius = 1
    radius_padding = 0.3
    bond_label_font_size = 16
    outer_line_width = 3
    color_line_width = 8
    inner_line_width = 2
    core_dot_radius = 80

    # Formula/structure label
    label_offset = 0.5
    formula_font_size = 15
    formula_offset = -2.5
    for index, structure in enumerate(unique_structure_types):
        result = system_analysis.extract_structure_info(
            structure_dict, structure
        )
        formulas, bond_labels, bond_fractions = result
        formula = formula_parser.get_subscripted_formula(formulas[0])
        structure = formula_parser.get_subscripted_formula(structure)

        fig, ax = plt.subplots(figsize=(3, 3.5), dpi=300)
        plt.subplots_adjust(
            top=1.1
        )  # Adjust this value to reduce the space at the top

        hexagon.draw_hexagon_per_center_point(
            center_pt,
            bond_fractions,
            radius=radius,
            inner_alpha=0.3,
            outer_alpha=1,
            inner_line_width=inner_line_width,
            outer_line_width=outer_line_width,
            color_line_width=color_line_width,
            is_individual_hexagonal=is_individual_hexagonal,
        )

        plt.scatter(0, 0, color="black", s=core_dot_radius, zorder=3)

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
    #  plt.tight_layout()
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
        f"Saved individual hexagon images and a composite image in {output_dir}"
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

    # Show the plot
    plt.show()
    plt.close()

    # output_filepath = join(output_dir, "binary.png")
    # plt.savefig(output_filepath, dpi=300)
    # plt.close()
