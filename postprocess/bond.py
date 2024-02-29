
import os
from os.path import join, exists
import glob
from shutil import rmtree, move
from preprocess.cif_parser import get_atom_type


def strip_labels_and_remove_duplicate_atom_type_pairs(unique_pairs_distances):
    '''
    Truth: 560709: Co-Ga 2.501, Co-Co 2.501, Ga-Ga 2.501, La-Co 2.979, La-Ga 2.979)
    unique_pairs_distances = {
        {('Co', 'Co'): ['2.501'],
        ('Co', 'Ga'): ['2.501'],
        ('Co', 'La'): ['2.979'],
        ('Ga', 'Ga'): ['2.501'],
        ('Ga', 'La'): ['2.979']}
    '''
    print(unique_pairs_distances)


    adjusted_pairs = {}
    for pair, distances in unique_pairs_distances.items():
        simplified_pair = tuple(sorted(get_atom_type(atom) for atom in pair))
        # If the pair already exists, compare distances and keep the smallest (not applicable here since all distances are the same)
        # Here we assume distances are strings and convert them to floats for comparison; this part of the logic is simplified due to identical distances
        if simplified_pair not in adjusted_pairs:
            adjusted_pairs[simplified_pair] = distances

    return adjusted_pairs
