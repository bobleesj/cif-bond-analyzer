# The goal is determine the CN methods

import os
import time
import numpy as np
from coordination import handler as cn_handler
from coordination import calculator as cn_calculator
from coordination import polyhedron as cn_polyhedron
from coordination import structure as cn_structure
from coordination import angle as cn_angle
from coordination import geometry_handler

from coordination import optimize, data
from util import folder, prompt, formula_parser
from preprocess import cif_parser
from postprocess.environment import environment_util
from collections import Counter
from scipy.spatial import ConvexHull


file_path = "20250604_CN_4_methods/URhIn.cif"
formula = "URhIn"

all_labels_connections = cn_handler.get_connected_points(
    file_path, cut_off_radius=10
)
# Use dummby values for all radius?

"""
Step 1. Get connection dict data for URhIn with cutoff distance of 10
"""
shortest_dists_per_pair = (
    environment_util.get_pair_distances_dict_for_binary_ternary(
        all_labels_connections, formula
    )
)

min_dist_per_pair = {}
for key, distances in shortest_dists_per_pair.items():
    min_dist_per_pair[key] = min(distances)

"""
Step 2. Get 4 radius sum types
"""

rad_sum = None

sorted_formula = formula_parser.get_mendeleev_sorted_formula(formula)
if len(sorted_formula) == 3:
    R = sorted_formula[0]
    M = sorted_formula[1]
    X = sorted_formula[2]
    elements = (R, M, X)
    atom_radii = data.get_atom_radii(elements, data.get_radii_data())
    R_CIF_rad, R_Pauling_rad = atom_radii[R]["CIF"], atom_radii[R]["Pauling"]
    M_CIF_rad, M_Pauling_rad = atom_radii[M]["CIF"], atom_radii[M]["Pauling"]
    X_CIF_rad, X_Pauling_rad = atom_radii[X]["CIF"], atom_radii[X]["Pauling"]
    CIF_rads_refined = optimize.optimize_CIF_rad_ternary(
        R_CIF_rad, M_CIF_rad, X_CIF_rad, min_dist_per_pair
    )
    CIF_rads = (R_CIF_rad, M_CIF_rad, X_CIF_rad)
    Pauling_rads = (R_Pauling_rad, M_Pauling_rad, X_Pauling_rad)
    rad_sum = data.compute_rad_sum_ternary(
        CIF_rads, CIF_rads_refined, Pauling_rads, elements
    )

"""
Step 3. Find coordination number with 4 method
"""
max_gaps_per_label = cn_calculator.compute_normalized_dists_in_connections(
    rad_sum, all_labels_connections
)

"""
Step 4. Find the best polyhedron from each label
"""
best_polyhedrons = geometry_handler.find_best_polyhedron(
    max_gaps_per_label, all_labels_connections
)

"""
Step 5. Filter 
"""

"""
Step 6. Filter connected points based on CN
"""
CN_connections = geometry_handler.get_CN_connections(
    best_polyhedrons, all_labels_connections
)

environment_util.print_conneted_points(CN_connections)

prompt.print_dict_in_json(best_polyhedrons)

"""
Step 7. Find all angles between
"""

# Test for In1 for only
angles = cn_angle.compute_angles_from_central_atom(CN_connections)
# print(angles)

"""
Step 8. Get 180 angles atom index
"""
near_180_degrees_atom_indices = cn_angle.get_near_180_angle_atom_indices(
    angles
)

"""
Step 9. Find the coordinates 
"""

# cn_polyhedron.plot_polyhedrons(near_180_degrees_atom_indices, CN_connections)

"""
Step 10. Determine the number of atoms in each ring
"""

ring_counts = cn_structure.get_ring_count_above_below_central_atom_z(
    near_180_degrees_atom_indices, CN_connections
)
print(ring_counts)
