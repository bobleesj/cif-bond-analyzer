import random
import numpy as np
from util import formula_parser
import matplotlib.pyplot as plt


def hexagon_points_line_figure(center, size):
    """Generate points for a hexagon rotated to stand on a vertex."""
    angles = (
        np.linspace(0, 2 * np.pi, 7, endpoint=True) + np.pi / 6
    )  # Rotate by 30 degrees
    x_hex = center[0] + size * np.cos(angles)
    y_hex = center[1] + size * np.sin(angles)
    return x_hex, y_hex


# Function to create rotated hexagon points
def hexagon_points(center, size):
    """Generate the vertices of a regular hexagon given a center and size."""
    angle = np.radians(60)
    return [
        (
            center[0] + size * np.cos(i * angle),
            center[1] + size * np.sin(i * angle),
        )
        for i in range(6)
    ]


def draw_hexagons(bond_fractions, bond_types):
    formula = bond_fractions[0]
    AA_fraction = bond_fractions[1][0]
    AB_fraction = bond_fractions[1][1]
    BB_fraction = bond_fractions[1][2]

    print(formula, AA_fraction, AB_fraction, BB_fraction)

    # Calculate the hexagon points
    center = (0, 0)  # Center of the hexagon
    size = 1  # Distance from center to each vertex
    points = hexagon_points(center, size)

    # Rotate the hexagon 90 degrees to stand on a vertex
    rotation_angle = np.radians(
        -90
    )  # Negative for clockwise rotation
    rotation_matrix = np.array(
        [
            [np.cos(rotation_angle), -np.sin(rotation_angle)],
            [np.sin(rotation_angle), np.cos(rotation_angle)],
        ]
    )
    rotated_points = [rotation_matrix.dot(point) for point in points]

    # Separate the x and y coordinates
    x, y = zip(*rotated_points)

    # plt.fill(x, y, "b", alpha=0.3)  # Hexagon area

    # Create the plot again
    fig, ax = plt.subplots(figsize=(8, 8))

    # Starting angle at the bottom left (-30 degrees)
    starting_angle = 7 * np.pi / 6

    # Number of vertices for a hexagon
    num_vertices = 6

    # Generate the vertices of the hexagon
    theta = np.linspace(
        starting_angle,
        2 * np.pi + starting_angle,
        num_vertices,
        endpoint=False,
    )
    x = np.cos(theta)
    y = np.sin(theta)

    # Append the first x and y to close the hexagon shape
    x_closed = np.append(x, x[0])
    y_closed = np.append(y, y[0])

    AA = bond_types[0]
    AB = bond_types[1]
    BB = bond_types[2]
    # Check if it's a binary compound
    labels = [AA, AB, BB]
    transparency_indices = [3, 4, 5]
    colors = ["blue", "red", "green", "magenta", "yellow", "cyan"]

    #     labels = [
    #         "Co-Co",
    #         "Co-In",
    #         "In-In",
    #         "Co-Ru",
    #         "In-Ru",
    #         "Ru-Ru",
    #     ]
    #     transparency_indices = []

    # Get overlay lenghtsa based on fraction

    lenghts = [random.uniform(0, 1) for _ in labels]
    # lenghts = [AA_fraction, AB_fraction, BB_fraction]

    # Draw hexagon outline
    ax.plot(x_closed, y_closed, "-", lw=2, color="black")

    # Draw lines from the origin to each vertex, with some possibly transparent
    for i in range(len(x)):
        alpha_value = 0.1 if i in transparency_indices else 0.3
        ax.plot([0, x[i]], [0, y[i]], "k-", alpha=alpha_value)

    # Overlay thicker lines with random lengths,
    for i, length in enumerate(lenghts):
        ax.plot(
            [0, x[i] * length],
            [0, y[i] * length],
            lw=2.2,
            color=colors[i],
        )

    offset_factor = 0.2
    # Add offset labels to the vertices, with some possibly transparent
    for i, label in enumerate(labels):
        label_x = x[i] * (1 + offset_factor)
        label_y = y[i] * (1 + offset_factor)
        alpha_value = 0.1 if i in transparency_indices else 1
        ax.text(
            label_x,
            label_y,
            # f"{label}. {i}",
            f"{label}",
            fontsize=10,
            ha="center",
            va="center",
            alpha=alpha_value,
        )

    # Set limits and aspect ratio
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")  # Turn off the axis
    ax.set_title(formula, fontsize=12)

    # Show the plot
    plt.show()


def draw_horizontal_line_with_marks(bond_fractions_list, bond_types):
    fig, ax = plt.subplots()  # Create a figure and an axes.

    # Sample parsed formulas
    # parsed_formulas = [
    #     ("CoIn2", [("Co", 0.333), ("In", 0.667)]),
    #     ("CoIn3", [("Co", 0.250), ("In", 0.750)]),
    # ]

    print(bond_fractions_list)

    # Draw the horizontal line
    ax.plot(
        [0, 1], [0, 0], "k-", lw=2
    )  # Single line for both markers

    # Add labels at the ends of the line, adjust horizontal alignment
    ax.text(
        0,
        0,
        "Co",
        fontsize=12,
        ha="right",
        va="center",
        backgroundcolor="white",
    )
    ax.text(
        1,
        0,
        "In",
        fontsize=12,
        ha="left",
        va="center",
        backgroundcolor="white",
    )

    my_parsed_formulas = []
    # Place marks along the line
    for bond_fractions in bond_fractions_list:
        labels = bond_fractions[0]
        normalized_formula = formula_parser.get_normalized_formula(
            labels
        )
        parsed_normalized_formula = formula_parser.get_parsed_formula(
            normalized_formula
        )
        my_parsed_formulas.append((labels, parsed_normalized_formula))

    for formula, labels in my_parsed_formulas:
        # Find the position for 'In' from the formula and place a marker
        for element, fraction_str in labels:
            fraction = float(fraction_str)
            if element == "In":
                ax.plot(
                    fraction,
                    0,
                    "ro",
                    label=f"{formula}",
                )  # Place marker at the fraction
                ax.text(
                    fraction,
                    0.05,
                    f"{formula}",
                    fontsize=7,
                    ha="center",
                    va="bottom",
                )

    # Set limits to slightly beyond the ends to ensure visibility of labels and markers
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.2, 0.2)

    # Remove axes and ticks
    ax.axis("off")

    # Show the plot
    plt.show()


# import matplotlib.pyplot as plt
# import numpy as np


def draw_rotated_hexagons_along_line(bond_fractions_list):
    # Define figure size and DPI
    fig, ax = plt.subplots(
        figsize=(10, 3), dpi=100
    )  # DPI specifies the resolution of the figure

    # Draw a horizontal line
    ax.plot([0, 1], [0, 0], "k-", lw=2)

    # Add end labels
    ax.text(0, -0.05, "Co", fontsize=12, ha="right", va="center")
    ax.text(1, -0.05, "In", fontsize=12, ha="left", va="center")

    # Colors for the bottom three lines
    bottom_colors = ["blue", "red", "green"]
    line_width = 1

    # Draw hexagons based on bond fractions and connect from center to vertices with colored lines
    for bond_fractions in bond_fractions_list:
        formula = bond_fractions[0]
        normalized_formula = formula_parser.get_normalized_formula(
            formula
        )
        parsed_normalized_formula = formula_parser.get_parsed_formula(
            normalized_formula
        )
        # Generate random bond lengths for the three highlighted lines
        bond_lengths = [random.uniform(0, 1) for _ in range(3)]

        # Find the position for 'In' and draw a hexagon there
        for element, fraction_str in parsed_normalized_formula:
            if element == "In":
                fraction = float(fraction_str)
                # Calculate hexagon center based on the fraction along the horizontal line
                hex_center = (fraction, 0)
                x_hex, y_hex = hexagon_points_line_figure(
                    hex_center, 0.05
                )  # Smaller size for visibility on the plot

                # Draw the hexagon
                ax.plot(
                    x_hex, y_hex, "gray", lw=line_width, alpha=0.3
                )  # Hexagon edges

                # Draw lines from center to each vertex of the hexagon in specified colors
                for i, (x, y) in enumerate(
                    zip(x_hex[:-1], y_hex[:-1])
                ):
                    if i in [
                        3,
                        4,
                        5,
                    ]:  # Indices for the bottom vertices
                        color = bottom_colors[i - 3]
                        alpha = 1  # Opaque for highlighted lines
                        # Normalize the length of the line to the vertex based on provided bond lengths
                        norm_length = bond_lengths[i - 3]
                        ax.plot(
                            [
                                fraction,
                                fraction
                                + (x - fraction) * norm_length,
                            ],
                            [0, y * norm_length],
                            color=color,
                            lw=line_width,
                            alpha=alpha,
                        )

                    # Draw the other lines with high transparency in black
                    ax.plot(
                        [fraction, x],
                        [0, y],
                        color="black",
                        lw=line_width,
                        alpha=0.1,
                    )

                # Optional: label the hexagon
                ax.text(
                    hex_center[0],
                    hex_center[1] - 0.08,
                    formula,
                    fontsize=7,
                    ha="center",
                    va="top",
                )

    # Set limits and aspect
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.2, 0.2)
    # This ensures that the scale is the same on both axes
    ax.set_aspect("equal")
    ax.axis("off")
    plt.show()
