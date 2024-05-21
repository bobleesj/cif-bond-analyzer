import random
import numpy as np
from util import formula_parser, sort
import matplotlib.pyplot as plt
from postprocess.system_analysis import system_analysis
from postprocess.system_analysis.figure import hexagon, ternary


def draw_ternary_figure(structure_dict, unique_structure_types):
    formula_offset = -0.07
    formula_font_size = 9
    v0, v1, v2 = ternary.generate_traingle_vertex_points()

    ternary.draw_ternary_frame(v0, v1, v2)

    for structure in unique_structure_types:
        result = system_analysis.extract_structure_info(
            structure_dict, structure
        )
        formulas, _, bond_fractions = result
        formula = formulas[0]
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

        center_point = ternary.get_point_in_traingle_from_norm_index(
            v0, v1, v2, float(R_norm_index), float(M_norm_index)
        )
        hexagon.draw_hexagon_per_center_point(
            center_point, bond_fractions
        )
        # Write one of the chemical formulas
        plt.text(
            center_point[0],
            center_point[1] + formula_offset,
            formula,
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
    plt.close()


def draw_individual_hexagon(structure_dict, unique_structure_types):
    # Get a hexagon points
    center_pt = (0, 0)
    for structure in unique_structure_types:
        result = system_analysis.extract_structure_info(
            structure_dict, structure
        )
        formulas, bond_labels, bond_fractions = result
        formula = formulas[0]
        hexagon.draw_hexagon_per_center_point(
            center_pt, bond_fractions, radius=0.04
        )
        formula_offset = 0.05
        # Write one of the chemical formulas

        plt.text(
            center_pt[0],
            center_pt[1] + formula_offset,
            f"Formula: {formula}\nStructure: {structure}",
            fontsize=8,
            ha="center",
        )

        plt.scatter(
            center_pt[0], center_pt[1], color="black", s=5, zorder=3
        )
        x_hex_pts, y_hex_pts = hexagon.get_hexagon_points(
            center_pt, 0.05
        )
        # Place bond labels near each vertex
        label_offset = 0.02  # Distance from vertex to label
        for i, (x, y, label) in enumerate(
            zip(x_hex_pts, y_hex_pts, bond_labels)
        ):
            plt.text(
                x + label_offset * np.cos(i * np.pi / 3 + np.pi / 6),
                y + label_offset * np.sin(i * np.pi / 3 + np.pi / 6),
                label,
                fontsize=6,
                ha="center",
            )

        # Add label to each

        plt.gca().set_aspect("equal", adjustable="box")
        plt.axis("off")
        plt.show()
