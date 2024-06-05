from util import folder, prompt
from coordination import geometry as cn_geometry
from preprocess import cif_parser_handler, supercell_handler
from postprocess.environment import environment_neighbor
import numpy as np
from scipy.spatial import ConvexHull


def find_best_polyhedron(max_gaps_per_label, all_labels_connections):
    """
    Find the best polyhedron for each label based on the minimum
    distance between the reference atom to the avg. position of
    connected atoms.
    """
    best_polyhedrons = {}

    for label, CN_data_per_method in max_gaps_per_label.items():
        # Initialize variables to track the best polyhedron
        min_distance_to_center = float("inf")
        best_polyhedron_metrics = None
        best_method_used = (
            None  # Track which method was used for the best metrics
        )

        # Loop through each method
        for method, CN_data in CN_data_per_method.items():
            connection_data = all_labels_connections[label][: CN_data["CN"]]
            polyhedron_points = []
            central_atom_coord = []

            # Extract the necessary data from connections
            for connection in connection_data:
                if len(connection) > 3:
                    central_atom_coord = connection[2]
                    polyhedron_points.append(connection[3])

            try:
                hull = ConvexHull(polyhedron_points)
                polyhedron_points = np.array(polyhedron_points)
                polyhedron_metrics = cn_geometry.compute_polyhedron_metrics(
                    polyhedron_points, central_atom_coord, hull
                )

                # Check if the current polyhedron has the lowest distance to center
                if (
                    polyhedron_metrics["distance_from_avg_point_to_center"]
                    < min_distance_to_center
                ):
                    min_distance_to_center = polyhedron_metrics[
                        "distance_from_avg_point_to_center"
                    ]
                    best_polyhedron_metrics = polyhedron_metrics
                    best_method_used = (
                        method  # Record the method that produced these metrics
                    )

            except Exception as e:
                print(
                    f"\nError in determining polyhedron for {label}: {str(e)}\n"
                )
                continue

        if best_polyhedron_metrics:
            best_polyhedron_metrics[
                "method_used"
            ] = best_method_used  # Add method information to the metrics
            best_polyhedrons[label] = best_polyhedron_metrics

    return best_polyhedrons


def get_CN_connections(best_polyhedrons, all_labels_connections):
    """
    Retrieves connections limited by the number of vertices (CN_value) for each label.
    """
    CN_connections = {}

    for label, data in best_polyhedrons.items():
        CN_value = data[
            "number_of_vertices"
        ]  # Extract the limit for the number of vertices
        # Limit the connections for this label using CN_value
        CN_connections[label] = all_labels_connections[label][:CN_value]

    return CN_connections
