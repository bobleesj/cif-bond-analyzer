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
from util import prompt, formula_parser, folder
from preprocess import cif_parser
from postprocess.environment import env_util
from preprocess import format
from filter import occupancy


def run_coordination(file_path_list):
    for file_path in file_path_list:
        (
            _,
            formula,
            _,
            _,
        ) = cif_parser.get_phase_tag_formula_id_from_third_line(file_path)

        all_labels_connections = cn_handler.get_connected_points(
            file_path, cut_off_radius=10.0
        )

        """
        Step 1. Get connection dict data for URhIn with cutoff distance of 10
        """
        shortest_dists_per_pair = (
            env_util.get_pair_distances_dict_for_binary_ternary(
                all_labels_connections, formula
            )
        )

        """
        Step 2. Get 4 radius sum types
        """

        block = cif_parser.get_cif_block(file_path)

        cif_loop_values = cif_parser.get_loop_values(
            block, cif_parser.get_loop_tags()
        )
        # Get atomic site mixing info -> String

        # Check 1. only binary and ternary are possible
        num_of_elements = formula_parser.get_num_element(formula)

        # Check 1. For CIF and Pauling, check that the elements exist
        rad_sum = data_handler.compute_rad_sum(
            formula, shortest_dists_per_pair
        )
        is_rad_data_available = data_handler.check_element_exist_in_rad_data(
            formula
        )

        # Check 2. Atomic mixing is 4, full occupacny
        atom_site_mixing_file_type = occupancy.get_atom_site_mixing_info(
            cif_loop_values
        )
        max_gaps_per_label = None
        """
        Step 3. Find coordination number with 4 method
        """
        if (
            atom_site_mixing_file_type == "4"
            and is_rad_data_available
            and num_of_elements == 3
            or num_of_elements == 2
        ):
            max_gaps_per_label = (
                cn_calculator.compute_normalized_dists_with_methods(
                    rad_sum, all_labels_connections
                )
            )
        else:
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
