from preprocess.cif_parser import get_atom_type
import postprocess.pair_order as pair_order
from itertools import product
from util import prompt


def process_and_order_pairs(all_points, atomic_pair_list):
    '''
    Finds the shortest distance from each atom to another atom in the structure
    '''
    processed_pairs = []
    
    for i in range(len(all_points)):
        pair_point = i + 1

        shortest_pair = None
        shortest_distance = float('inf')

        for pair in atomic_pair_list:
            if pair_point in pair["point_pair"] and pair["distance"] < shortest_distance:
                shortest_distance = pair["distance"]
                shortest_pair = pair

        if shortest_pair is not None:
            processed_pairs.append(shortest_pair)
    
    # Ordering the processed pairs based on atom types
    processed_pairs_ordered = []
    for pair in processed_pairs:
        atom_type_0 = get_atom_type(pair['labels'][0])
        atom_type_1 = get_atom_type(pair['labels'][1])

        if atom_type_0 > atom_type_1:
            pair['labels'] = pair['labels'][::-1]
            pair['point_pair'] = pair['point_pair'][::-1]
            pair['coordinates'] = pair['coordinates'][::-1]

        processed_pairs_ordered.append(pair)

    return processed_pairs_ordered


def get_all_ordered_pairs_from_set(pair_dict):
    '''
    Generates all possible unique ordered label pairs.
    '''
    unique_labels = set()

    for pair in pair_dict.keys():
        element_1, element_2 = pair.split('-')
        unique_labels.add(element_1)
        unique_labels.add(element_2)

    # Generate all possible pairs (with ordering matter)
    all_pairs = list(product(unique_labels, repeat=2))

    # Order pairs based on Mendeleev ordering
    all_pairs_ordered = ([
        tuple(
            pair_order.order_pair_by_mendeleev(pair)
        ) for pair in all_pairs
    ])

    # Remove duplicates from all possible pairs
    all_pairs_ordered_unique = list(set(all_pairs_ordered))

    return all_pairs_ordered_unique


def get_sorted_missing_pairs(pair_dict):

    all_pairs = get_all_ordered_pairs_from_set(
        pair_dict
    )

    pairs_found = set(
        tuple(
            pair_order.order_pair_by_mendeleev(tuple(pair.split('-')))
        ) for pair in pair_dict.keys()
    )

    # Sort the pairs in the data as well before comparison
    missing_label_pairs = [
        pair for pair in all_pairs if pair not in pairs_found
    ]

    return missing_label_pairs


def get_unique_pairs_dict(ordered_pairs, filename):
    '''
    Constructs a dictionary containing the shortest distance pairs for each unique atom label pair
    per file. It iterates over a list of ordered pairs, where each pair
    contains atom labels and the distance between those atoms. If a pair of labels is encountered
    for the first time or if the current pair's distance is shorter than the previously recorded
    distance for the same label pair, it updates the dictionary to include the current pair.
    '''
    unique_pairs_dict = {}

    for pair in ordered_pairs:
        atom_label_0 = pair["labels"][0]
        atom_label_1 = pair["labels"][1]

        # Create a tuple of the labels
        label_tuple = (atom_label_0, atom_label_1)

        # Initialize a new dictionary for this filename
        if filename not in unique_pairs_dict:
            unique_pairs_dict[filename] = {}

        # If these labels have not been seen before or
        # if this pair is shorter than the previous pair
        if (label_tuple not in unique_pairs_dict[filename] or
            pair["distance"] < unique_pairs_dict[filename][label_tuple]["distance"]):

            # Add this pair to the dictionary
            unique_pairs_dict[filename][label_tuple] = pair

    return unique_pairs_dict


def get_dist_mix_pair_dict(dist_mix_pair_dict,
                           unique_pairs_dict,
                           label_pair_mixing_dict):
    """
    Returns dict containing files and dist per pair.
    """
    for filename, pairs in unique_pairs_dict.items():
        for labels, pair in pairs.items():
            pair_tuple_ordered = pair_order.order_pair_by_mendeleev(
                (labels[0], labels[1])
            )
            label_1 = pair_tuple_ordered[0]
            label_2 = pair_tuple_ordered[1]
            dist = round(pair['distance'], 3)
            dist_str = str(dist)

            # Convert dist back to float for comparison
            pair_key = f"{label_1}-{label_2}"
            pair_mixing_category = label_pair_mixing_dict[pair_tuple_ordered]

            # Initialize pair_key if not exists
            if pair_key not in dist_mix_pair_dict:
                dist_mix_pair_dict[pair_key] = {}

            # Check if the file is already associated with the pair_key
            if filename in dist_mix_pair_dict[pair_key]:
                # Update only if the new distance is shorter
                if dist < float(dist_mix_pair_dict[pair_key][filename]["dist"]):
                    dist_mix_pair_dict[pair_key][filename] = {
                        "mixing": pair_mixing_category,
                        "dist": dist_str
                    }
            else:
                # If the file is not associated yet, add it directly
                dist_mix_pair_dict[pair_key][filename] = {
                    "mixing": pair_mixing_category,
                    "dist": dist_str
                }

    return dist_mix_pair_dict


def get_element_pair_from_label_pair(labels):
    '''
    Convert Ge1-Ge2 to Ge-Ge, for intance.
    '''
    labels = labels.split('-')
    element1 = get_atom_type(labels[0])
    element2 = get_atom_type(labels[1])
    return f"{element1}-{element2}"


def get_dist_mix_element_pair_dict(input_dict):
    output_dict = {}

    for pair_key, values in input_dict.items():
        new_key = get_element_pair_from_label_pair(pair_key)
        
        if new_key not in output_dict:
            output_dict[new_key] = {}

        for id, id_value in values.items():
            # Convert id_value to a list if it's not one already
            if id not in output_dict[new_key]:
                output_dict[new_key][id] = []
            # Check if the current id_value (as a dict) is already in the list
            # So if the mixing is different, it is stored
            if not any(v == id_value for v in output_dict[new_key][id]):
                output_dict[new_key][id].append(id_value)

    return output_dict
