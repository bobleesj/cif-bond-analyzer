from coordination import unary as cn_unary
from util import folder

# The goal is determine the CN methods
from coordination import handler as cn_handler

"""
Set up
"""

cif_dir = "20250605_Mo"
file_paths = folder.get_file_path_list(cif_dir)

# Collect all point groups
connected_points_group = []
file_paths = folder.get_file_path_list(cif_dir)
for file_path in file_paths:
    connected_points = cn_handler.get_connected_points(file_path)
    connected_points_group.append(connected_points)

"""
Method 1. Find the shortest distance basde CIF Rad (DONE)
"""
cif_rad_by_shortest_dist = cn_unary.compute_average_radius_by_shortest_dist(
    connected_points_group
)

"""
Method 2. Use d/d_min to find the CN
"""

# Compute the CN using d_min only for each CIF file
coordination_number = cn_unary.get_coordination_number_by_dist_min(
    connected_points_group
)
cif_rad_by_avg_from_center = (
    cn_unary.find_avg_radius_from_avg_dist_from_central_atom(
        coordination_number, connected_points_group
    )
)

print("\nWe are looking at", cif_dir)
print(
    "Method 1. Find cif radius based on shortest dist",
    cif_rad_by_shortest_dist,
)
print(
    "Method 2. Find cif radius based on avg dist from the center",
    cif_rad_by_avg_from_center,
)
print()
