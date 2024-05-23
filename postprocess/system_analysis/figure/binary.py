import numpy as np
from util import formula_parser
import matplotlib.pyplot as plt
from postprocess.system_analysis.figure import hexagon


def draw_horizontal_lines_with_multiple_marks(norm_bond_count_dict):
    fig, ax = plt.subplots()  # Create a figure and an axes only once.

    # Draw the horizontal line
    ax.plot([0, 1], [0, 0], "k-", lw=2)
    # Process each formula
    for formula, bond_counts in norm_bond_count_dict.items():
        parsed_normalized_formula = (
            formula_parser.get_parsed_norm_formula(formula)
        )
        A_label, _ = parsed_normalized_formula[0]
        B_label, B_norm_index = parsed_normalized_formula[1]

        bond_fractions = list(bond_counts.values())
        marker_position = float(B_norm_index)
        center_pt = [marker_position, 0]
        hexagon.draw_single_hexagon_and_lines_per_center_point(
            center_pt,
            bond_fractions,
            is_binary=True,
            is_for_individual_hexagon=False,
        )

        # Add labels for the first and last element
        ax.text(
            0,
            -0.1,
            A_label,
            fontsize=12,
            ha="right",
            va="center",
            backgroundcolor="white",
        )
        ax.text(
            1,
            -0.1,
            B_label,
            fontsize=12,
            ha="left",
            va="center",
            backgroundcolor="white",
        )

        # Draw the marker for this formula
        ax.plot(
            float(marker_position),
            0,
            "ko",
            markersize=4,
            label=f"{formula} ({B_label})",
        )
        ax.text(
            float(marker_position),
            0.05,
            f"{formula}",
            fontsize=7,
            ha="center",
            va="bottom",
        )

    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.5, 0.2)
    plt.gca().set_aspect("equal", adjustable="box")
    ax.axis("off")
