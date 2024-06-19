import json
from cifkit import CifEnsemble
from collections import defaultdict
import postprocess.pair_order as pair_order
import itertools
from cifkit.utils import string_parser


"""
 Each pair of site labels is sorted
 alphabetically and converted into a tuple. A dictionary (min_distances)
 is used to track the minimum distance observed for each unique sorted pair.
 As the script iterates through each pair's distance,
 it checks whether this pair is already recorded in min_distances.
 If the pair is new, or if a shorter distance for an existing
 pair is found, the dictionary is updated accordingly.
 """

cif_ensemble = CifEnsemble(
    "tests/data/20240611_ternary_binary_combined_cifkit"
)


def process_cif_files(cif_ensemble):
    data = {}
    for cif in cif_ensemble.cifs:
        print("Processing", cif.file_name)
        shortest_distances = cif.shortest_site_pair_distance

        # Alphabetically sort the label pair and find min distance per unique pair
        unique_label_pair_distances = {}
        for site_label, (other_label, distance) in shortest_distances.items():
            sorted_pair = tuple(sorted((site_label, other_label)))
            if (
                sorted_pair not in unique_label_pair_distances
                or unique_label_pair_distances[sorted_pair] > distance
            ):
                unique_label_pair_distances[sorted_pair] = distance

        # Get site unique label pair data sorted by mendeleev
        for pair, distance in unique_label_pair_distances.items():
            site_element = string_parser.get_atom_type_from_label(pair[0])
            other_element = string_parser.get_atom_type_from_label(pair[1])
            sorted_pair = pair_order.order_pair_by_mendeleev(
                (site_element, other_element)
            )
            bond_key = f"{sorted_pair[0]}-{sorted_pair[1]}"
            if bond_key not in data:
                data[bond_key] = {}
            if cif.file_name_without_ext not in data[bond_key]:
                data[bond_key][cif.file_name_without_ext] = []
            data[bond_key][cif.file_name_without_ext].append(
                {"dist": distance}
            )
    return data


def clean_dictionary(data):
    """Remove keys with empty data"""
    cleaned_data = {}
    for bond, cif_dict in data.items():
        if cif_dict:
            cleaned_data[bond] = cif_dict
        else:
            print(f"Removed empty bond pair: {bond}")
    return cleaned_data


def save_to_json(data, json_file_path):
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Data has been saved to {json_file_path}.")


def calculate_minimum_distances(data):
    """Return the minimum distance per pair."""
    min_distances = {}
    for bond, cif_dict in data.items():
        min_distances[bond] = {}
        for cif_id, distances in cif_dict.items():
            min_distance = min(distances, key=lambda x: x["dist"])
            min_distances[bond][cif_id] = [min_distance]
    return min_distances


# Main workflow
site_unique_label_pair_data = process_cif_files(cif_ensemble)
cleaned_data = clean_dictionary(site_unique_label_pair_data)
save_to_json(cleaned_data, "site_site_pair_data.json")
site_unique_element_pair_data = calculate_minimum_distances(cleaned_data)
save_to_json(site_unique_element_pair_data, "site_element_pair_data.json")


"""
Mendeleeve number:
Er 35
Co	58
In	75
"""

"""
Processing 1956508.cif
Er Co1 2.799
In2 Co2 2.687
In1 In2 2.949
Co2 In2 2.687
Co1 Er 2.799

From here, notice In2 Co2 is identical as Co2 and In2, therefore, 
a single value of 2.687 and its sorted pair should be kept.

Er Co1 2.799
In2 Co2 2.687
In1 In2 2.949
"""

"""
Step 4. Implement atomic mixing from CIF Ensemble
"""

"""
Step 5. Now, find the element site info then
"""
