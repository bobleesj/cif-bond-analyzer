import os
from core.util import formula_parser
import matplotlib.pyplot as plt
from core.system import hexagon
from core.system.figure_util import parse_bond_fractions_formulas
from core.prompts.progress import prompt_file_saved


def draw_binary_figure(bond_fractions_data, output_dir, is_CN_used):
    """
    Draw binary figures from bond fractions, save as PNG based on CN usage.
    """
    # In the case of 3 bond fractions (2 elements)
    for _, data in bond_fractions_data.items():
        (
            bond_fractions,
            bnod_fractions_CN,
            _,
            formulas,
        ) = parse_bond_fractions_formulas(data)
        if is_CN_used:
            draw_horizontal_lines_with_multiple_marks(
                formulas[0],
                bnod_fractions_CN,
            )
        else:
            draw_horizontal_lines_with_multiple_marks(
                formulas[0],
                bond_fractions,
            )

    # Save figure
    if is_CN_used:
        output_filename = "binary_single_CN.png"
    else:
        output_filename = "binary_single.png"

    output_filepath = os.path.join(output_dir, output_filename)
    plt.savefig(output_filepath, dpi=300)
    prompt_file_saved(output_filepath)
    plt.close()


def draw_horizontal_lines_with_multiple_marks(
    formula,
    bond_fractions,
):
    # Draw the horizontal line
    plt.plot([0, 1], [0, 0], "k-", lw=2)

    parsed_normalized_formula = formula_parser.get_parsed_norm_formula(formula)
    A_label, _ = parsed_normalized_formula[0]
    B_label, B_norm_index = parsed_normalized_formula[1]
    marker_position = float(B_norm_index)
    center_pt = [marker_position, 0]

    hexagon.draw_single_hexagon_and_lines_per_center_point(
        center_pt,
        bond_fractions,
    )

    # Add labels for the first and last element
    plt.text(
        0,
        -0.1,
        A_label,
        fontsize=12,
        ha="right",
        va="center",
        backgroundcolor="white",
    )
    plt.text(
        1,
        -0.1,
        B_label,
        fontsize=12,
        ha="left",
        va="center",
        backgroundcolor="white",
    )

    # Draw the marker for this formula
    plt.plot(
        float(marker_position),
        0,
        "ko",
        markersize=3,
        zorder=5,
        label=f"{formula} ({B_label})",
    )

    plt.text(
        float(marker_position),
        0.05,
        f"{formula}",
        fontsize=7,
        ha="center",
        va="bottom",
    )

    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.5, 0.2)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.axis("off")
