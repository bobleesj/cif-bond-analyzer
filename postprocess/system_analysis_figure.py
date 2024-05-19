import random
import numpy as np
import re
from fractions import Fraction
import matplotlib.pyplot as plt


def get_element_fractions(compound_formulas_in_dict):
    # Get fraction of atoms from the formula
    fractions_dict = {}

    for formula in compound_formulas_in_dict:
        # Find all capital letters followed by any digits, using regex
        elements_counts = re.findall(r"([A-Z][a-z]*)(\d*)", formula)
        fractions_info = {}

        # Initialize count for each element
        element_counts = {
            element: int(count) if count else 1
            for element, count in elements_counts
        }

        # Calculate fraction of element B (In)
        total_atoms = sum(element_counts.values())
        fraction_B = Fraction(
            element_counts["In"], total_atoms
        ).limit_denominator()
        fractions_info["fraction_B"] = np.round(float(fraction_B), 3)

        # Store in dictionary
        fractions_dict[formula] = fractions_info
    return fractions_dict


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


def draw_line(structure_dict):
    # Parse the two formula CoIn2 and CoIn3
    # Get all the

    is_binary = None
    is_ternary = None

    bond_pairs_in_dict = []
    compound_formulas_in_dict = []
    for formula, structures in structure_dict.items():
        compound_formulas_in_dict.append(formula)
        for structure, bonds in structures.items():
            for bond, data in bonds.items():
                bond_pairs_in_dict.append(bond)
    unique_bond_pairs_in_dict = len(set(bond_pairs_in_dict))

    # Check whether the system is binary or ternary
    if unique_bond_pairs_in_dict == 3:
        print("This is a binary system")
        is_binary = True
    elif unique_bond_pairs_in_dict == 6:
        print("This is a ternary system")
        is_ternary = True
    else:
        print("This is not a either binary or ternary. Terminate.")
        return

    # Output the dictionary to check results
    fractions_dict = get_element_fractions(compound_formulas_in_dict)
    print(fractions_dict)

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

    # Check if it's a binary compound
    is_binary = True
    if is_binary:
        labels = ["Co-Co", "Co-In", "In-In"]
        transparency_indices = [
            3,
            4,
            5,
        ]  # Indices for the vertices to make transparent
    else:
        labels = [
            "Co-Co",
            "Co-In",
            "In-In",
            "Co-Ru",
            "In-Ru",
            "Ru-Ru",
        ]
        transparency_indices = []

    # Get random overlay lenghts
    random_lengths = [random.uniform(0, 1) for _ in labels]
    # Draw the hexagon outline (ensure it is closed)
    ax.plot(
        x_closed, y_closed, "o-", lw=2
    )  # Hexagon outline and vertices

    # Draw lines from the origin to each vertex, with some possibly transparent
    for i in range(len(x)):
        alpha_value = 0.1 if i in transparency_indices else 0.8
        ax.plot(
            [0, x[i]], [0, y[i]], "k-", alpha=alpha_value
        )  # Base lines to vertices

    # Overlay thicker lines with random lengths, with some possibly transparent
    for i, length in enumerate(random_lengths):
        alpha_value = 0.1 if i in transparency_indices else 1
        ax.plot(
            [0, x[i] * length],
            [0, y[i] * length],
            "k-",
            lw=2.2,
            alpha=alpha_value,
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

    # Show the plot
    plt.show()

    # Add colors for each bond
    # Generate a sample dict
    # Generate a horizontal graph
