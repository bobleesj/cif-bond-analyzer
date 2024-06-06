from coordination import optimize, data
from util import folder, prompt, formula_parser
from preprocess import cif_parser
from postprocess.environment import env_util
from collections import Counter
from scipy.spatial import ConvexHull


def compute_rad_sum(formula, shortest_dists_per_pair):
    sorted_formula = formula_parser.get_mendeleev_sorted_formula(formula)
    min_dist_per_pair = {}
    for key, distances in shortest_dists_per_pair.items():
        min_dist_per_pair[key] = min(distances)

    if len(sorted_formula) == 3:
        return compute_rad_sum_ternary(sorted_formula, min_dist_per_pair)

    if len(sorted_formula) == 2:
        return compute_rad_sum_binary(sorted_formula, min_dist_per_pair)


def compute_rad_sum_ternary(sorted_formula, min_dist_per_pair):
    R = sorted_formula[0]
    M = sorted_formula[1]
    X = sorted_formula[2]
    elements = (R, M, X)
    atom_radii = data.get_atom_radii(elements, data.get_radii_data())
    R_CIF_rad, R_Pauling_rad = (
        atom_radii[R]["CIF"],
        atom_radii[R]["Pauling"],
    )
    M_CIF_rad, M_Pauling_rad = (
        atom_radii[M]["CIF"],
        atom_radii[M]["Pauling"],
    )
    X_CIF_rad, X_Pauling_rad = (
        atom_radii[X]["CIF"],
        atom_radii[X]["Pauling"],
    )
    CIF_rads_refined = optimize.optimize_CIF_rad_ternary(
        R_CIF_rad, M_CIF_rad, X_CIF_rad, min_dist_per_pair
    )
    CIF_rads = (R_CIF_rad, M_CIF_rad, X_CIF_rad)
    Pauling_rads = (R_Pauling_rad, M_Pauling_rad, X_Pauling_rad)
    rad_sum = data.compute_rad_sum_ternary(
        CIF_rads, CIF_rads_refined, Pauling_rads, elements
    )
    return rad_sum


def compute_rad_sum_binary(sorted_formula, min_dist_per_pair):
    A = sorted_formula[0]
    B = sorted_formula[1]
    elements = (A, B)

    atom_radii = data.get_atom_radii(elements, data.get_radii_data())
    A_CIF_rad, A_Pauling_rad = (
        atom_radii[A]["CIF"],
        atom_radii[A]["Pauling"],
    )
    B_CIF_rad, B_Pauling_rad = (
        atom_radii[B]["CIF"],
        atom_radii[B]["Pauling"],
    )
    CIF_rads_refined = optimize.optimize_CIF_rad_binary(
        A_CIF_rad, B_CIF_rad, min_dist_per_pair
    )
    CIF_rads = (A_CIF_rad, B_CIF_rad)
    Pauling_rads = (A_Pauling_rad, B_Pauling_rad)
    rad_sum = data.compute_rad_sum_binary(
        CIF_rads, CIF_rads_refined, Pauling_rads, elements
    )
    return rad_sum
