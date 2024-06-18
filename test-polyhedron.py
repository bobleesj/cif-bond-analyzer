import pyvista as pv
import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial import Delaunay

points = np.array(
    [
        [0.0, 0.0, 3.881],
        [0.0, 0.0, 0.0],
        [3.738, 2.158, 1.94],
        [3.738, -2.158, 1.94],
        [4.43, 0.0, 0.0],
        [4.43, 0.0, 3.881],
        [-0.936, 1.622, 1.94],
        [-0.936, -1.622, 1.94],
        [1.523, 2.638, 0.0],
        [1.523, -2.638, 0.0],
        [1.523, -2.638, 3.881],
        [1.523, 2.638, 3.881],
        [1.873, 0.0, -1.94],
        [1.873, 0.0, 5.821],
        [1.873, 0.0, 1.94],
    ]
)

vertex_labels = [
    "Rh2",
    "Rh2",
    "Rh1",
    "Rh1",
    "U1",
    "U1",
    "In1",
    "In1",
    "U1",
    "U1",
    "U1",
    "U1",
    "In1",
    "In1",
    "In1",
]

plotter = pv.Plotter()

central_atom_index = np.argmin(
    np.linalg.norm(points, axis=1)
)
central_atom = points[central_atom_index]

for point, label in zip(points, vertex_labels):
    radius = (
        0.6 if np.array_equal(point, central_atom) else 0.4
    )  # Central atom larger
    sphere = pv.Sphere(radius=radius, center=point)
    plotter.add_mesh(
        sphere, color="#D3D3D3"
    )  # Light grey color


delaunay = Delaunay(points)
hull = ConvexHull(points)

edges = set()
for simplex in delaunay.simplices:
    for i in range(4):
        for j in range(i + 1, 4):
            edge = tuple(sorted([simplex[i], simplex[j]]))
            edges.add(edge)

hull_edges = set()
for simplex in hull.simplices:
    for i in range(len(simplex)):
        for j in range(i + 1, len(simplex)):
            hull_edge = tuple(
                sorted([simplex[i], simplex[j]])
            )
            hull_edges.add(hull_edge)

for edge in edges:
    if edge in hull_edges:
        start, end = points[edge[0]], points[edge[1]]
        cylinder = pv.Cylinder(
            center=(start + end) / 2,
            direction=end - start,
            radius=0.05,
            height=np.linalg.norm(end - start),
        )
        plotter.add_mesh(cylinder, color="grey")

faces = []
for simplex in hull.simplices:
    faces.append([3] + list(simplex))
poly_data = pv.PolyData(points, faces)

plotter.add_mesh(
    poly_data, color="aqua", opacity=0.5, show_edges=True
)
plotter.show()
