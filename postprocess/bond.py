from os.path import join, exists
from shutil import rmtree, move
from preprocess.cif_parser import get_atom_type


def strip_labels_and_remove_duplicate_atom_type_pairs(unique_pairs_distances):
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
        current_distance = float(distances[0])  # Convert distance to float for comparison

        # If the pair already exists, compare distances and keep the smallest
        if simplified_pair in adjusted_pairs:
            existing_distance = float(adjusted_pairs[simplified_pair][0])
            if current_distance < existing_distance:
                adjusted_pairs[simplified_pair] = [distances[0]]
        else:
            adjusted_pairs[simplified_pair] = distances

    return adjusted_pairs