# The goal is determine the CN methods

import os
import time
from coordination import handler as cn_handler
from coordination import calculator as cn_calculator
from coordination import optimize, data
from util import folder, prompt
from preprocess import cif_parser
from postprocess.environment import environment_util

file_path = "20250604_CN_4_methods/URhIn.cif"
all_labels_connections = cn_handler.get_connected_points(
    file_path, cut_off_radius=10
)
# Use dummby values for all radius?

"""
Step 1. Get connection dict data for URhIn with cutoff distance of 10
"""
print(prompt.log_conneted_points(all_labels_connections))
formula = "URhIn"


shortest_dists_per_pair = (
    environment_util.get_pair_distances_dict_for_binary_ternary(
        all_labels_connections, formula
    )
)

min_dist_per_pair = {}
for key, distances in shortest_dists_per_pair.items():
    min_dist_per_pair[key] = min(distances)

"""
Here {'RR': 3.881, 'MM': 3.881, 'XX': 3.244, 'RM': 2.983, 'MX': 2.697, 'RX': 3.21}
SAF INT_UNI_shortest_homoatomic_dist 3.24367, shortest_heteroatomic_dist 2.69678   
"""

"""
Step 2. Get 4 radius types
"""
R = "U"
M = "Rh"
X = "In"
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
rad_sum_ternary = data.compute_rad_sum_ternary(
    CIF_rads, CIF_rads_refined, Pauling_rads, elements
)

# Step 3. Find coordination number with 4 method
max_gaps_per_label = cn_calculator.compute_normalized_dists_in_connections(
    rad_sum_ternary, all_labels_connections
)

for label, cn_per_method in max_gaps_per_label.items():
    print(label)
    print(cn_per_method)

# Step 4.
