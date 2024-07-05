import numpy as np
import os
from core.util import formula_parser
import matplotlib.pyplot as plt
from core.prompts.progress import prompt_file_saved
from core.system import hexagon
from core.system.figure_util import parse_bond_fractions_formulas


def draw_hexagon_for_individual_figure(
    bond_fractions_data, output_dir, elements, is_CN_used
):
    """
    Draw individual hexagons
    """

    if is_CN_used:
        individuals_dir = os.path.join(output_dir, "individuals_CN")
        os.makedirs(individuals_dir, exist_ok=True)
    else:
        individuals_dir = os.path.join(output_dir, "individuals")
        os.makedirs(individuals_dir, exist_ok=True)

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

    formulas_no_tag_for_hexagon_binary = []
    formulas_no_tag_for_hexagon_ternary = []
    hexagon_image_files_binary = []
    hexagon_image_files_ternary = []
    contain_binary = False
    contain_ternary = False

    for structure, data in bond_fractions_data.items():
        (
            bond_fractions,
            bnod_fractions_CN,
            bond_pairs,
            formulas,
        ) = parse_bond_fractions_formulas(data)

        structure = formula_parser.get_subscripted_string(structure)
        elements_parsed_from_formula = formula_parser.get_unique_elements(formulas[0])
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
        x_label_pts, y_label_pts = hexagon.get_hexagon_points(center_pt, label_radius)

        # Find minimum and maximum for both x and y from the hexagon points
        x_min, x_max = min(x_label_pts), max(x_label_pts)
        y_min, y_max = min(y_label_pts), max(y_label_pts)

        ax.set_xlim(x_min - radius_padding, x_max + radius_padding)
        ax.set_ylim(y_min - radius_padding, y_max + radius_padding)

        for i, (x, y, label) in enumerate(zip(x_label_pts, y_label_pts, bond_pairs)):
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

        is_binary_file = len(elements_parsed_from_formula) == 2
        formula_no_tag = formula_parser.remove_tag_with_underscore(formulas[0])

        # Saving each hexagon to a file
        if is_binary_file:
            hexagon_filename = f"bi_{formulas[0]}.png"
        else:
            hexagon_filename = f"ter_{formulas[0]}.png"

        hexagon_filepath = os.path.join(individuals_dir, hexagon_filename)
        fig.savefig(hexagon_filepath, dpi=300)
        plt.close(fig)

        if is_binary_file:
            hexagon_image_files_binary.append(hexagon_filepath)
            formulas_no_tag_for_hexagon_binary.append(formula_no_tag)
            contain_binary = True
        else:
            hexagon_image_files_ternary.append(hexagon_filepath)
            formulas_no_tag_for_hexagon_ternary.append(formula_no_tag)
            contain_ternary = True

        # Add the formula used, without thet ag
        # formulas_no_tag_for_hexagon.append(formula_no_tag)

    """
    Save composite figures files
    - We need to order the hexagons by normalized fraction of X, M, etc.
    """

    parsed_norm_formulas_binary = [
        formula_parser.get_parsed_norm_formula(formula)
        for formula in formulas_no_tag_for_hexagon_binary
    ]
    parsed_norm_formulas_ternary = [
        formula_parser.get_parsed_norm_formula(formula)
        for formula in formulas_no_tag_for_hexagon_ternary
    ]
    # Case 1. Only contain binary files
    if contain_binary and not contain_ternary:
        A, B = formula_parser.get_AB_from_elements(elements)
        sorted_indices_binary = get_sorted_indices_by_binary_elements(
            parsed_norm_formulas_binary, B, A
        )
        sorted_files_binary = [
            hexagon_image_files_binary[i] for i in sorted_indices_binary
        ]
        save_single_composite_figures(sorted_files_binary, True, is_CN_used, output_dir)

    # Case 2. Contain only ternary files
    if contain_ternary:
        R, M, X = formula_parser.get_RMX_from_elements(elements)
        sorted_indices_ternary = get_sorted_indices_by_ternary_elements(
            parsed_norm_formulas_ternary, X, M, R
        )

        sorted_files_ternary = [
            hexagon_image_files_ternary[i] for i in sorted_indices_ternary
        ]
        save_single_composite_figures(
            sorted_files_ternary, False, is_CN_used, output_dir
        )
        # Case 3. Contain both binary and ternary files
        if contain_binary:
            sorted_indices_binary = get_sorted_indices_by_binary_elements(
                parsed_norm_formulas_binary, X, M
            )
            sorted_files_binary = [
                hexagon_image_files_binary[i] for i in sorted_indices_binary
            ]
            save_single_composite_figures(
                sorted_files_binary, True, is_CN_used, output_dir
            )


def save_single_composite_figures(
    sorted_hexagon_image_files, is_binary, is_CN_used, output_dir
):
    """
    Save multiple composite figures from hexagon images based on CN and type.
    """

    # Constants for the layout
    max_images_per_figure = 12
    rows_per_figure = 4
    cols_per_figure = 3

    # Calculate the number of figures needed
    num_figures = int(np.ceil(len(sorted_hexagon_image_files) / max_images_per_figure))
    # # Loop through each figure to be created
    for fig_idx in range(num_figures):
        # Calculate the range of images for this figure
        start_idx = fig_idx * max_images_per_figure
        end_idx = min(
            (fig_idx + 1) * max_images_per_figure,
            len(sorted_hexagon_image_files),
        )
        current_images = sorted_hexagon_image_files[start_idx:end_idx]

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
        if is_binary and is_CN_used:
            composite_filepath = os.path.join(
                output_dir, f"composite_binary_{fig_idx+1}_CN.png"
            )
        elif is_binary and not is_CN_used:
            composite_filepath = os.path.join(
                output_dir, f"composite_binary_{fig_idx+1}.png"
            )
        elif not is_binary and is_CN_used:
            composite_filepath = os.path.join(
                output_dir, f"composite_ternary_{fig_idx+1}_CN.png"
            )
        elif not is_binary and not is_CN_used:
            composite_filepath = os.path.join(
                output_dir, f"composite_ternary_{fig_idx+1}.png"
            )
        fig.savefig(composite_filepath, dpi=300)
        plt.close(fig)
        prompt_file_saved(composite_filepath)


def get_sorted_indices_by_binary_elements(
    parsed_formulas, primary_element, secondary_element
):
    """
    Sort indices by primary and secondary element fractions in binary formulas.
    """
    element_data = []

    # Collect the relevant fractions for primary and secondary elements
    for index, parsed_formula in enumerate(parsed_formulas):
        element_dict = dict(parsed_formula)

        primary_fraction = float(element_dict.get(primary_element, 0))
        secondary_fraction = float(element_dict.get(secondary_element, 0))

        element_data.append((index, primary_fraction, secondary_fraction))

    # Sort by primary element fraction, then by secondary element fraction
    element_data.sort(key=lambda x: (x[1], x[2]))

    # Extract the original indices in sorted order
    sorted_indices = [index for index, _, _ in element_data]

    return sorted_indices


def get_sorted_indices_by_ternary_elements(
    parsed_formulas, primary_element, secondary_element, tertiary_element
):
    """
    Sort indices by element fractions in ternary formulas.
    """
    element_data = []

    # Collect the relevant fractions for primary, secondary, and tertiary elements
    for index, parsed_formula in enumerate(parsed_formulas):
        element_dict = dict(parsed_formula)

        # Get fractions, default to 0 if the element is not found
        primary_fraction = float(element_dict.get(primary_element, 0))
        secondary_fraction = float(element_dict.get(secondary_element, 0))
        tertiary_fraction = float(element_dict.get(tertiary_element, 0))

        element_data.append(
            (index, primary_fraction, secondary_fraction, tertiary_fraction)
        )

    # Sort by primary element fraction, then by secondary, then by tertiary
    element_data.sort(key=lambda x: (x[1], x[2], x[3]))

    # Extract the original indices in sorted order
    sorted_indices = [index for index, _, _, _ in element_data]

    return sorted_indices
