from preprocess.cif_parser import get_atom_type
import postprocess.pair_order as pair_order
from itertools import product

def process_and_order_pairs(all_points, atomic_pair_list):
    '''
    Find the shortest distance from each atom to another 
    atom in the structure
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


def strip_labels_and_remove_duplicate(unique_pairs_distances):
    '''
    unique_pairs_distances_test_2 = {
        ('Ga1A', 'Ga1'): ['2.601'],
        ('Ga1', 'La1'): ['3.291'],
        ('Co1B', 'Ga1'): ['2.601'],
        ('Ga1', 'Ga1A'): ['2.601'],
        ('Ga1', 'Ga1'): ['2.358']}

    to 

    adjusted_pairs_test_2 == {
        ('Ga', 'Ga'): ['2.358'],
        ('Ga', 'La'): ['3.291'],
        ('Co', 'Ga'): ['2.601']}

    '''

    adjusted_pairs = {}
    for pair, distances in unique_pairs_distances.items():

        current_distance = float(distances[0])

        # If the pair already exists, compare distances and keep the smallest
        if pair in adjusted_pairs:
            existing_distance = float(adjusted_pairs[pair][0])
            if current_distance < existing_distance:
                adjusted_pairs[pair] = [distances[0]]
        else:
            adjusted_pairs[pair] = distances

    return adjusted_pairs


def get_sorted_missing_pairs(adjusted_unique_pairs_distances):
    # Extract all unique elements from the pairs
    unique_elements = list(set([element for pair in adjusted_unique_pairs_distances.keys() for element in pair]))

    # Generate all possible pairs (with ordering matter)
    # Assuming unique_elements is a list of unique chemical elements
    all_possible_pairs = list(product(unique_elements, repeat=2))

    # Order pairs based on Mendeleev ordering
    all_possible_pairs = (
        [tuple(pair_order.order_pair_based_on_mendeleev_num(pair)) for pair in all_possible_pairs]
    )

    print(all_possible_pairs, "all_possible_pairs\n")

    # Remove duplicates after sorting
    all_possible_pairs = list(set(all_possible_pairs))

    # Sort the pairs in the data as well before comparison
    pair_list = [tuple((pair)) for pair in adjusted_unique_pairs_distances.keys()]

    # Find the pairs that are not in the data
    missing_pair_list = [pair for pair in all_possible_pairs if pair not in pair_list]

    return pair_list, missing_pair_list


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


def get_unique_pairs_distances(global_pairs_data):
    unique_pairs_distances = {}
    for filename, pairs in global_pairs_data.items():
        for pair, dist in pairs.items():
            if pair not in unique_pairs_distances:
                unique_pairs_distances[pair] = [dist]
            else:
                unique_pairs_distances[pair].append(dist)
    return unique_pairs_distances
