import os

import matplotlib.pyplot as plt

from core.configs.ternary import TernaryConfig
from core.prompts.progress import prompt_file_saved
from core.system import ternary
from core.system.figure_util import parse_bond_fractions_formulas
from core.util import formula_parser


def draw_ternary_figure(
    bond_fraction_per_structure_data,
    bond_pairs_ordered,
    formulas_no_tag,
    formulas_with_tag,
    RMX,
    output_dir,
    is_CN_used,
):
    """Draw ternary diagrams with bond fractions and save to specified
    directory."""
    # Grid
    grid_alpha = 0.2
    grid_line_width = 0.5

    # Triangle frame
    vertices = ternary.generate_triangle_vertex_points()
    v0, v1, v2 = vertices
    ternary.draw_ternary_frame(v0, v1, v2)
    ternary.draw_filled_edges(v0, v1, v2)
    ternary.draw_triangular_grid(
        v0, v1, v2, grid_alpha, grid_line_width, n_lines=10
    )

    # Legend
    ternary.draw_legend(
        bond_pairs_ordered,
        TernaryConfig.X_SHIFT.value,
        TernaryConfig.Y_SHIFT.value,
    )

    # Vertex label
    ternary.add_vertex_labels(v0, v1, v2, RMX)
    """Draw each hexagon point on the triangle."""

    # Get all unique formulas
    for _, data in bond_fraction_per_structure_data.items():
        (
            bond_fractions,
            bnod_fractions_CN,
            _,
            formulas,
        ) = parse_bond_fractions_formulas(data)
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
                formulas_no_tag,
                parsed_normalized_formula,
                bond_fractions,
                bnod_fractions_CN,
                formula,
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
    prompt_file_saved(output_filepath)
    plt.close()
