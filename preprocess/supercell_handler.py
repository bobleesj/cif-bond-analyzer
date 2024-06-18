from preprocess import cif_parser, supercell


def get_flattened_points_from_unitcell(file_path):
    loop_tags = cif_parser.get_loop_tags()
    cif_block = cif_parser.get_cif_block(file_path)
    cif_loop_values = cif_parser.get_loop_values(
        cif_block, loop_tags
    )
    all_coords_list = supercell.get_coords_list(
        cif_block, cif_loop_values
    )
    points, _, _ = supercell.get_points_and_labels(
        all_coords_list,
        cif_loop_values,
        is_flatten_points_only=True,
    )
    return points
