from preprocess import cif_parser_handler, supercell_handler
from postprocess.environment import environment_neighbor


def get_connected_points(file_path, cut_off_radius=5.0):
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
    return all_labels_connections
