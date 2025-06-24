import time
from cifkit import CifEnsemble
from cifkit.utils.string_parser import get_atom_type_from_label
from cifkit.utils.bond_pair import order_tuple_pair_by_mendeleev
from core.prompts.progress import (
    prompt_progress_current,
    prompt_progress_finished,
)


def get_site_pair_data_ordered_by_mendeleev(cif_ensemble: CifEnsemble):
    """
    Sort each pair of site labels alphabetically, converting to a tuple.
    Track the minimum distance for each unique sorted pair in a dictionary.
    Update the dictionary if a new pair is found or a shorter distance for an
    existing pair is recorded.
    """

    data = {}
    file_count = cif_ensemble.file_count
    for i, cif in enumerate(cif_ensemble.cifs, start=1):
        start_time = time.perf_counter()
        prompt_progress_current(i, cif.file_name, cif.supercell_atom_count, file_count)
        cif.compute_CN()
        try:
            mixing_info = cif.mixing_info_per_label_pair_sorted_by_mendeleev
            shortest_distances = cif.shortest_site_pair_distance
        except Exception as e:
            print(f"Error occured processing {cif.file_name}: {e}")
            continue

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
        for label_pair, distance in unique_label_pair_distances.items():
            site_element = get_atom_type_from_label(label_pair[0])
            other_element = get_atom_type_from_label(label_pair[1])

            ordered_label_pair = order_tuple_pair_by_mendeleev(label_pair)
            ordered_element_pair = order_tuple_pair_by_mendeleev(
                (site_element, other_element)
            )

            bond_key = f"{ordered_element_pair[0]}-{ordered_element_pair[1]}"

            if bond_key not in data:
                data[bond_key] = {}

            if cif.file_name_without_ext not in data[bond_key]:
                data[bond_key][cif.file_name_without_ext] = []

            # Get mixing info per pair
            mixing_status = mixing_info.get(ordered_label_pair, "unknown")

            # Append
            data[bond_key][cif.file_name_without_ext].append(
                {
                    "dist": distance,
                    "mixing": mixing_status,
                    "formula": cif.formula,
                    "tag": cif.tag,
                    "structure": cif.structure,
                }
            )

        # Record time
        elapsed_time = time.perf_counter() - start_time

        prompt_progress_finished(cif.file_name, cif.supercell_atom_count, elapsed_time)
    remove_empty_keys(data)

    return data


def remove_empty_keys(data):
    """
    Remove keys with empty data.
    """
    cleaned_data = {}
    for bond, cif_dict in data.items():
        if cif_dict:
            cleaned_data[bond] = cif_dict
        # else:
        #     print(f"Removed empty bond pair: {bond}")
    return cleaned_data


def filter_with_minimum_distance_per_file(data):
    """
    Return the minimum distance per pair.
    """
    min_distances = {}
    for bond, cif_dict in data.items():
        min_distances[bond] = {}
        for cif_id, distances in cif_dict.items():
            min_distance = min(distances, key=lambda x: x["dist"])
            min_distances[bond][cif_id] = [min_distance]
    return min_distances


#
