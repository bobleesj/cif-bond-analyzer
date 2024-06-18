# The goal is determine the CN methods

import os
import time
from coordination import polyhedron as cn_polyhedron
from coordination import structure as cn_structure
from coordination import angle as cn_angle
from preprocess import format


# """
# Step 6. Find all angles between
# """

# angles = cn_angle.compute_angles_from_central_atom(CN_connections)

# """
# Step 7. Get 180 angles atom index
# """
# largest_angle_atom_indices = (
#     cn_angle.get_largest_angle_atom_indices_largest_to_smallest(angles)
# )

# prompt.log_conneted_points(all_labels_connections)
# """
# Step 8. Find the coordinates
# """

# cn_polyhedron.plot_polyhedrons(
#     largest_angle_atom_indices, angles, CN_connections, file_path
# )
