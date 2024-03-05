from preprocess.cif_parser import get_atom_type
from itertools import permutations


def process_and_order_pairs(all_points, atomic_pair_list):
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
        simplified_pair = tuple(sorted(get_atom_type(atom) for atom in pair))
        current_distance = float(distances[0])

        # If the pair already exists, compare distances and keep the smallest
        if simplified_pair in adjusted_pairs:
            existing_distance = float(adjusted_pairs[simplified_pair][0])
            if current_distance < existing_distance:
                adjusted_pairs[simplified_pair] = [distances[0]]
        else:
            adjusted_pairs[simplified_pair] = distances

    return adjusted_pairs


def get_sorted_missing_pairs(adjusted_unique_pairs_distances):
    # Extract all unique elements from the pairs
    unique_elements = list(set([element for pair in adjusted_unique_pairs_distances.keys() for element in pair]))

    # Generate all possible pairs (with ordering matter)
    all_possible_pairs = list(permutations(unique_elements, 2))

    # Make sure each pair is sorted
    all_possible_pairs = [tuple(sorted(pair)) for pair in all_possible_pairs]

    # Remove duplicates after sorting
    all_possible_pairs = list(set(all_possible_pairs))

    # Sort the pairs in the data as well before comparison
    sorted_pair_list = [tuple(sorted(pair)) for pair in adjusted_unique_pairs_distances.keys()]

    # Find the pairs that are not in the data
    missing_pair_list = [pair for pair in all_possible_pairs if pair not in sorted_pair_list]

    missing_pair_list = sorted(missing_pair_list, key=lambda x: x)
    return sorted_pair_list, missing_pair_list


def get_unique_pairs_dict(ordered_pairs, filename):
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
