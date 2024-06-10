from util import folder, prompt
from coordination import geometry as cn_geometry
from preprocess import cif_parser_handler, supercell_handler, cif_parser
from postprocess.environment import environment_neighbor
import numpy as np
from scipy.spatial import ConvexHull


def get_connected_points(file_path, cut_off_radius):
    result = cif_parser_handler.get_cif_info(file_path)
    (
        _,
        lengths,
        angles,
        _,
        supercell_points,
        labels,
        _,
    ) = result

    unitcell_points = supercell_handler.get_flattened_points_from_unitcell(
        file_path
    )
    all_labels_connections = environment_neighbor.get_all_labels_connections(
        labels,
        unitcell_points,
        supercell_points,
        cut_off_radius,
        lengths,
        angles,
    )

    all_labels_connections = (
        environment_neighbor.remove_duplicates_based_on_coord2(
            all_labels_connections
        )
    )

    return all_labels_connections
