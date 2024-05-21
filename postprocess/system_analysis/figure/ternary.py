import numpy as np
import random
import matplotlib.pyplot as plt


def get_point_in_traingle_from_norm_index(
    v0, v1, v2, R_norm_index, M_norm_index
):
    R = R_norm_index
    M = M_norm_index

    if R + M > 1:
        R = 1 - R
        M = 1 - M
    return (1 - R - M) * v0 + M * v1 + R * v2


def generate_traingle_vertex_points():
    v0 = np.array([0, 0])
    v1 = np.array([1, 0])
    v2 = np.array([0.5, np.sqrt(3) / 2])
    return v0, v1, v2


def draw_ternary_frame(v0, v1, v2):
    # Triangle vertices
    # Plotting the enhanced triangle
    plt.figure(figsize=(8, 7))
    triangle = plt.Polygon(
        [v0, v1, v2], edgecolor="k", facecolor="none"
    )
    # Draw edges of the traingle
    plt.gca().add_patch(triangle)

    # Draw traingular grid
    draw_triangular_grid(v0, v1, v2, n_lines=10)


def add_vertex_labels(v0, v1, v2, labels):
    # Labeling the vertices
    plt.text(
        v0[0] - 0.02,
        v0[1] - 0.02,
        labels[0],
        fontsize=14,
        ha="right",
        va="top",
    )
    plt.text(
        v1[0] + 0.02,
        v1[1] - 0.02,
        labels[1],
        fontsize=14,
        ha="left",
        va="top",
    )
    plt.text(
        v2[0],
        v2[1] + 0.02,
        labels[2],
        fontsize=14,
        ha="center",
        va="bottom",
    )

    # Setting limits and aspect
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.axis("off")
    plt.show()


def draw_triangular_grid(v0, v1, v2, n_lines=10):
    # Line parallel to v2v0 (right slant)
    alpha = 0.2
    line_width = 0.5
    for i in range(1, n_lines):
        t = i / n_lines

        # Compute intermediate points on the edges
        p0 = (1 - t) * v0 + t * v1  # from v0 to v1
        p1 = (1 - t) * v0 + t * v2  # from v0 to v2
        p2 = (1 - t) * v1 + t * v2  # from v1 to v2
        p3 = (t) * v1 + (1 - t) * v2  # from v1 to v2

        plt.plot(
            [p0[0], p3[0]],
            [p0[1], p3[1]],
            "k",
            alpha=alpha,
            lw=line_width,
        )
        # Line parallel to v1v2 (left slant)
        plt.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            "k",
            alpha=alpha,
            lw=line_width,
        )
        # Line parallel to v0v1 (base)
        plt.plot(
            [p0[0], p1[0]],
            [p0[1], p1[1]],
            "k",
            alpha=alpha,
            lw=line_width,
        )
