import numpy as np
import os
from core.util import formula_parser
import matplotlib.pyplot as plt
from core.system import structure_util
from core.system import hexagon
from core.system.figure_util import parse_bond_fractions_formulas


def draw_hexagon_for_individual_figure(
    bond_fractions_data, output_dir, is_CN_used
):

    if is_CN_used:
        individuals_dir = os.path.join(output_dir, "individuals_CN")
        os.makedirs(individuals_dir, exist_ok=True)
    else:
        individuals_dir = os.path.join(output_dir, "individuals")
        os.makedirs(individuals_dir, exist_ok=True)

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

    for structure, data in bond_fractions_data.items():
        bond_fractions, bnod_fractions_CN, bond_pairs, formulas = (
            parse_bond_fractions_formulas(data)
        )

        structure = formula_parser.get_subscripted_string(structure)
        formula = formula_parser.get_subscripted_string(formulas[0])

        fig, ax = plt.subplots(figsize=(3, 3.5), dpi=300)
        plt.subplots_adjust(top=1.1)

        if is_CN_used:

            hexagon.draw_single_hexagon_and_lines_per_center_point(
                center_pt,
                bnod_fractions_CN,
                radius=radius,
                hex_inner_color="#D3D3D3",
                hex_outer_color="black",
                hex_inner_line_width=inner_line_width,
                hex_outer_line_width=outer_line_width,
                color_line_width=color_line_width,
                is_for_individual_hexagon=True,
            )
        else:
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
        # Add a black dot in the middle
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
            zip(x_label_pts, y_label_pts, bond_pairs)
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
        if is_CN_used:
            composite_filepath = os.path.join(
                output_dir, f"composite_{fig_idx+1}_CN.png"
            )
        else:
            composite_filepath = os.path.join(
                output_dir, f"composite_{fig_idx+1}.png"
            )
        fig.savefig(composite_filepath, dpi=300)
        plt.close(fig)
        print(f"Saved composite hexagon image {fig_idx+1} in {output_dir}")
