# The goal is determine the CN methods

import os
import time
import numpy as np
from coordination import handler as cn_handler
from coordination import calculator as cn_calculator
from coordination import polyhedron as cn_polyhedron
from coordination import structure as cn_structure
from coordination import angle as cn_angle
from coordination import geometry_handler as cn_geom_handler
from coordination import data_handler
from util import prompt, formula_parser
from preprocess import cif_parser
from postprocess.environment import env_util
from preprocess import format

format.preprocess_move_files_based_on_format_error("20250604_CN_4_methods")
file_path = "20240610_CN_12_14/528296_CN12_not_easy.cif"

_, formula, _, cif_id = cif_parser.get_phase_tag_formula_id_from_third_line(
    file_path
)

all_labels_connections = cn_handler.get_connected_points(
    file_path, cut_off_radius=10.0
)

"""
Step 1. Get connection dict data for URhIn with cutoff distance of 10
"""
shortest_dists_per_pair = env_util.get_pair_distances_dict_for_binary_ternary(
    all_labels_connections, formula
)

"""
Step 2. Get 4 radius sum types
"""

sorted_formula = formula_parser.get_mendeleev_sorted_formula(formula)
rad_sum = data_handler.compute_rad_sum(formula, shortest_dists_per_pair)


"""
Step 3. Find coordination number with 4 method
# """
max_gaps_per_label = cn_calculator.compute_normalized_dists(
    rad_sum, all_labels_connections
)

"""
Step 4. Find the best polyhedron from each label
"""
best_polyhedrons = cn_geom_handler.find_best_polyhedron(
    max_gaps_per_label, all_labels_connections
)

prompt.print_dict_in_json(best_polyhedrons)
"""
Step 5. Filter connected points based on CN
"""
CN_connections = cn_geom_handler.get_CN_connections(
    best_polyhedrons, all_labels_connections
)

"""
Step 6. Find all angles between
"""

angles = cn_angle.compute_angles_from_central_atom(CN_connections)

"""
Step 7. Get 180 angles atom index
"""
largest_angle_atom_indices = (
    cn_angle.get_largest_angle_atom_indices_largest_to_smallest(angles)
)

prompt.log_conneted_points(all_labels_connections)
"""
Step 8. Find the coordinates
"""

cn_polyhedron.plot_polyhedrons(
    largest_angle_atom_indices, angles, CN_connections, file_path
)
