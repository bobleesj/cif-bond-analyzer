import numpy as np
import os
from core.util import formula_parser, prompt
import matplotlib.pyplot as plt
from core.system import structure_util, ternary
from core.system import hexagon
from core.system.figure_util import (
    parse_bond_fractions_formulas,
)


def draw_ternary_figure(
    bond_fraction_per_structure_data,
    bond_pairs_ordered,
    unique_formulas,
    RMX,
    output_dir,
    is_CN_used,
):

    # Grid
    grid_alpha = 0.2
    grid_line_width = 0.5

    # Trinagle frame
    vertices = ternary.generate_traingle_vertex_points()
    v0, v1, v2 = vertices
    ternary.draw_ternary_frame(v0, v1, v2)
    ternary.draw_extra_frame_for_binary_tags(v0, v1, v2, unique_formulas, RMX)
    ternary.draw_filled_edges(v0, v1, v2)
    ternary.draw_triangular_grid(
        v0, v1, v2, grid_alpha, grid_line_width, n_lines=10
    )

    # Legend
    ternary.draw_legend(bond_pairs_ordered, x_position=0.0)

    # Vertex label
    # Add vertex label using ternary formula
    ternary.add_vertex_labels(v0, v1, v2, RMX)

    """
    Draw each hexagon point on the traingle.
    """

    # Get all unique formulas
    for _, data in bond_fraction_per_structure_data.items():
        bond_fractions, bnod_fractions_CN, _, formulas = (
            parse_bond_fractions_formulas(data)
        )
        formula = formulas[0]
        parsed_normalized_formula = formula_parser.get_parsed_norm_formula(
            formula
        )

        num_of_elements = formula_parser.get_num_element(formula)

        if num_of_elements == 3:
            center_pt = ternary.draw_hexagon_for_ternary_formula(
                vertices,
                parsed_normalized_formula,
                bond_fractions,
                bnod_fractions_CN,
                is_CN_used,
            )

        # For binary - shift center position with tags
        if num_of_elements == 2:
            tag = formula_parser.extract_tag(formula)
            center_pt = ternary.draw_hexagon_for_binary_formula(
                vertices,
                parsed_normalized_formula,
                bond_fractions,
                bnod_fractions_CN,
                RMX,
                tag,
                is_CN_used,
            )

        # Add formula and dot for each hexagon
        ternary.draw_center_dot_formula(center_pt, formula)

    # Save figure
    if is_CN_used:
        output_filepath = os.path.join(output_dir, "ternary_CN.png")
    else:
        output_filepath = os.path.join(output_dir, "ternary.png")

    plt.axis("off")
    plt.savefig(output_filepath, dpi=300)
    plt.close()
