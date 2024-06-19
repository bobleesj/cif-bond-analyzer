import numpy as np
from util import formula_parser
from os.path import join
import matplotlib.pyplot as plt
from postprocess.system.figure import hexagon


def draw_horizontal_lines_with_multiple_marks(
    formula,
    bond_fractions_per_formula,
    structures,
    is_single_binary,
):
    # Draw the horizontal line
    plt.plot([0, 1], [0, 0], "k-", lw=2)

    for i, _ in enumerate(structures):
        parsed_normalized_formula = formula_parser.get_parsed_norm_formula(
            formula
        )

        A_label, _ = parsed_normalized_formula[0]
        B_label, B_norm_index = parsed_normalized_formula[1]
        marker_position = float(B_norm_index)
        center_pt = [marker_position, 0]
        hexagon.draw_single_hexagon_and_lines_per_center_point(
            center_pt,
            bond_fractions_per_formula[i],
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
