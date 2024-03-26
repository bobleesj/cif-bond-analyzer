"""
This module offers functions for molecular structure analysis, focusing on
processing, ordering, and analyzing atom pairs within CIF data. Capabilities
include processing and ordering atom pairs by distance, generating all possible
unique ordered label pairs, identifying missing pairs not in CIF data,
building dictionaries with shortest distance pairs and their mixing categories,
and converting label to element pairs for analysis.
"""
import json
import numpy as np

from preprocess.cif_parser import get_atom_type
from preprocess import supercell
from postprocess import pair_order
from util import prompt


def get_atom_site_labeled_dict(
    all_points, lengths, angles, atom_site_mixing_dict, filename
):
    """
    Calculate the shortest distance from each atomic site and store only the labels
    of the pairs with the same minimum distance.
    """

    atom_site_dict = {}

    for i, point_1 in enumerate(all_points):
        current_site_label = point_1[3]

        if current_site_label not in atom_site_dict:
            atom_site_dict[current_site_label] = {
                "min_dist": float("inf"),
                "pairs": [],
            }

        for j, point_2 in enumerate(all_points):
            if i == j:
                continue  # Skip the identical index

            dist_result = supercell.calculate_dist(
                point_1, point_2, lengths, angles
            )
            dist, _, label_2 = dist_result
            dist = abs(
                np.round(dist, 3)
            )  # Round and take absolute value of the distance

            if dist < 0.01:
                continue

            if dist < atom_site_dict[current_site_label]["min_dist"]:
                atom_site_dict[current_site_label]["min_dist"] = dist
                atom_site_dict[current_site_label]["pairs"] = [label_2]
            elif dist == atom_site_dict[current_site_label]["min_dist"]:
                # Add the label to the pairs list if it's not already included
                if label_2 not in atom_site_dict[current_site_label]["pairs"]:
                    atom_site_dict[current_site_label]["pairs"].append(label_2)

    """
    Processing 1830597.cif with 333 atoms (1/1)
    {
    "Ga1": {
        "min_dist": 2.424,
        "pairs": [
            "Ni1"
        ]
    },
    "Ga2": {
        "min_dist": 2.53,
        "pairs": [
            "Ni2"
        ]
    },
    "Ni1": {
        "min_dist": 2.424,
        "pairs": [
            "Ga1"
        ]
    },
    "Ni2": {
        "min_dist": 2.53,
        "pairs": [
            "Ni3",
            "Ga2"
        ]
    },
    "Ni3": {
        "min_dist": 2.477,
        "pairs": [
            "Ni1"
        ]
    }
    }"""

    atom_site_dict_postprocessed = postprocess_atom_site_dict(
        atom_site_dict, atom_site_mixing_dict, filename
    )

    return atom_site_dict_postprocessed


def transform_to_list(atom_site_dict):
    """
    Transform the atom_site_dict into a list of tuples in the form of (site1, site2, min_dist).
    """
    pairs_list = []
    for site, info in atom_site_dict.items():
        min_dist = info["min_dist"]
        for pair in info["pairs"]:
            pairs_list.append((site, pair, min_dist))
    return pairs_list


def postprocess_atom_site_dict(
    atom_site_dict, atom_site_mixing_dict, filename
):
    pairs_list = transform_to_list(atom_site_dict)
    atom_site_dict_processed = {}

    for site1, site2, min_dist in pairs_list:
        # Use the order_pair_by_mendeleev to order the pair
        ordered_pair = pair_order.order_pair_by_mendeleev((site1, site2))
        pair_label = f"{ordered_pair[0]}-{ordered_pair[1]}"

        # Determine the mixing value from atom_site_mixing_dict
        mixing = atom_site_mixing_dict[
            tuple([ordered_pair[0], ordered_pair[1]])
        ]

        if pair_label not in atom_site_dict_processed:
            atom_site_dict_processed[pair_label] = {}

        if filename not in atom_site_dict_processed[pair_label]:
            atom_site_dict_processed[pair_label][filename] = []

        entry = {"dist": f"{min_dist:.3f}", "mixing": mixing}

        # Append the data and avoid duplicates
        if entry not in atom_site_dict_processed[pair_label][filename]:
            atom_site_dict_processed[pair_label][filename].append(entry)

    # prompt.print_dict_in_json(atom_site_dict_processed)

    return atom_site_dict_processed


def get_shortest_distance(values):
    """
    Finds the shortest distance value and corresponding mixing value from a list of values
    """
    shortest_dist = None
    shortest_mixing = None
    for value in values:
        distance = float(value["dist"])
        mixing = int(value["mixing"])
        if shortest_dist is None or distance < shortest_dist:
            shortest_dist = distance
            shortest_mixing = mixing
    return shortest_dist, shortest_mixing


def get_atom_site_dict_with_no_number(input_dict):
    """
    Strips numbers in each label and collection pairs
    """
    output_dict = {}
    for pair_key, values in input_dict.items():
        element_pair_key = get_element_pair_from_label_pair(pair_key)
        output_dict.setdefault(element_pair_key, {})
        for id, id_values in values.items():
            output_dict[element_pair_key].setdefault(id, [])
            for value in id_values:
                if value not in output_dict[element_pair_key][id]:
                    output_dict[element_pair_key][id].append(value)
    return output_dict


def get_element_dict(input_dict):
    """
    Strips numbers in each label and collection pairs and finds the shortest distance value for each pair and ID while maintaining mixing information
    """
    output_dict = {}
    for pair_key, values in input_dict.items():
        element_pair_key = get_element_pair_from_label_pair(pair_key)
        output_dict.setdefault(element_pair_key, {})
        for id, id_values in values.items():
            shortest_dist, shortest_mixing = get_shortest_distance(id_values)
            output_dict[element_pair_key][id] = [
                {"dist": str(shortest_dist), "mixing": str(shortest_mixing)}
            ]
    return output_dict


def append_atom_site_dict(global_atom_site_pair_dict, atom_site_pair_dict):
    """
    Appends atom_site_pair_dict to global_atom_site_pair_dict
    """

    for pair_key, values in atom_site_pair_dict.items():
        if pair_key not in global_atom_site_pair_dict:
            global_atom_site_pair_dict[pair_key] = {}

        for id, id_values in values.items():
            if id not in global_atom_site_pair_dict[pair_key]:
                global_atom_site_pair_dict[pair_key][id] = []

            for value in id_values:
                if value not in global_atom_site_pair_dict[pair_key][id]:
                    global_atom_site_pair_dict[pair_key][id].append(value)

    return global_atom_site_pair_dict


def append_element_site_dict(global_element_pair_dict, atom_site_pair_dict):
    """
    Appends element_site_pair to global_element_pair_dict
    """

    for pair_key, values in atom_site_pair_dict.items():
        if pair_key not in global_element_pair_dict:
            global_element_pair_dict[pair_key] = {}

        for id, id_values in values.items():
            if id not in global_element_pair_dict[pair_key]:
                global_element_pair_dict[pair_key][id] = []

            for value in id_values:
                if value not in global_element_pair_dict[pair_key][id]:
                    global_element_pair_dict[pair_key][id].append(value)

    return global_element_pair_dict


def get_element_pair_from_label_pair(labels):
    """
    Converts Ge1-Ge2 to Ge-Ge, for example.
    """
    labels = labels.split("-")
    element1 = get_atom_type(labels[0])
    element2 = get_atom_type(labels[1])
    return f"{element1}-{element2}"
