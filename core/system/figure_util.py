import os
import json
import numpy as np
import pandas as pd
import click
from core.util import prompt, formula_parser, string_parser
from core.system import structure_util


def get_bond_fractions_data_for_figures(
    cif_ensemble, structure_dict, bond_pairs_formatted
):
    """Return bond fractions (CN, site), formulas, for each structure"""
    bond_fractions_data: dict = {}

    for cif in cif_ensemble.cifs:
        structure = cif.structure

        if structure not in bond_fractions_data:
            # Initialize both dictionaries using the same ordered bond list
            ordered_bond_fractions = {
                bond: 0.0 for bond in bond_pairs_formatted
            }

            initial_bond_fractions = structure_dict[structure][
                "bond_fractions"
            ]
            # Ensures bonds are initialized in order
            bond_fractions_data[structure] = {
                "bond_fractions_CN": ordered_bond_fractions.copy(),
                "formulas": list(structure_dict[structure]["formulas"]),
                "bond_fractions": {
                    bond: initial_bond_fractions.get(bond, 0.0)
                    for bond in bond_pairs_formatted
                },
            }

        # Update the bond fractions for this CIF's structure
        bond_fractions = (
            cif.CN_bond_fractions_by_best_methods_sorted_by_mendeleev
        )

        for bond_tuple, fraction in bond_fractions.items():
            bond = f"{bond_tuple[0]}-{bond_tuple[1]}"
            if bond in bond_pairs_formatted:
                bond_fractions_data[structure]["bond_fractions_CN"][
                    bond
                ] = fraction

    return bond_fractions_data


def parse_bond_fractions_formulas(data):
    """Parse bond fractinos, pairs, formulas from each loop of plot data."""
    bond_fractions = list(data["bond_fractions"].values())
    bnod_fractions_CN = list(data["bond_fractions_CN"].values())
    bond_pairs = list(data["bond_fractions"].keys())
    formulas = data["formulas"]

    return bond_fractions, bnod_fractions_CN, bond_pairs, formulas


def get_hexagon_vertex_colors(is_pure_binary):
    if is_pure_binary:
        return ["blue", "cyan", "green"]
    else:
        return [
            "blue",
            "cyan",
            "green",
            "yellow",
            "red",
            "magenta",
        ]


def shift_points_xy(point, x_shift, y_shift=0):
    # Shift a point along the x-axis and y-axis
    return np.array([point[0] + x_shift, point[1] + y_shift])
