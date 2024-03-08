import preprocess.cif_parser as cif_parser
from itertools import product
import postprocess.pair_order as pair_order

def get_atom_info(CIF_loop_values, i):
    label = CIF_loop_values[0][i]
    occupancy = float(cif_parser.remove_string_braket(CIF_loop_values[7][i]))
    coordinates = (cif_parser.remove_string_braket(CIF_loop_values[4][i]),
                   cif_parser.remove_string_braket(CIF_loop_values[5][i]),
                   cif_parser.remove_string_braket(CIF_loop_values[6][i]))
    return label, occupancy, coordinates


def get_coord_occupancy_sum(CIF_loop_values):
    num_atom_labels = cif_parser.get_num_of_atom_labels(CIF_loop_values)
    # Check for full occupancy
    coord_occupancy_sum = {}

    for i in range(num_atom_labels):
        label, occupancy, coordinates = get_atom_info(CIF_loop_values, i)
        occupancy_num = coord_occupancy_sum.get(coordinates, 0) + occupancy
        coord_occupancy_sum[coordinates] = occupancy_num

    return coord_occupancy_sum


def get_atom_site_mixing_info(CIF_loop_values):
    is_full_occupancy = True

    coord_occupancy_sum = get_coord_occupancy_sum(CIF_loop_values)

    # Now check summed occupancies
    for coordinates, sum_occ in coord_occupancy_sum.items():
        if sum_occ != 1:
            is_full_occupancy = False
            print(f"Summed occupancy at {coordinates}: {sum_occ}")

    # Check for atomic mixing
    num_atom_labels = len(CIF_loop_values[0])
    is_atomic_mixing = len(coord_occupancy_sum) != num_atom_labels

    if is_atomic_mixing and not is_full_occupancy:
        # "deficiency"
        return "1"

    elif is_atomic_mixing and is_full_occupancy:
        # "full_occupancy_atomic_mixing"
        return "2"

    elif not is_atomic_mixing and not is_full_occupancy:
        # "deficiency_no_atomic_mixing"
        return "3"

    elif is_full_occupancy:
        # "full_occupancy"
        return "4"


def get_all_possible_ordered_label_pairs(CIF_loop_values):
    # Get a list of unique pairs from atomic labels
    label_list = cif_parser.get_atom_label_list(CIF_loop_values)
    all_possible_label_pairs = list(product(label_list, repeat=2))

    # Order label pairs using the Mendeleev number
    unique_ordered_label_pairs = []

    for pair_tuple in all_possible_label_pairs:
        # From all product, append half of the elements in order
        if pair_order.is_pair_ordered_by_mendeleev(pair_tuple):
            unique_ordered_label_pairs.append(pair_tuple)
    return unique_ordered_label_pairs


# Get atom site mixing label for all pairs possible
def get_atom_site_mixing_dict(
        atom_site_mixing_file_info, CIF_loop_values):

    atom_site_pair_dict = {}
    unique_ordered_label_pairs = get_all_possible_ordered_label_pairs(
        CIF_loop_values
    )

    # Case 4 full_occupancy
    if atom_site_mixing_file_info == "4":
        for pair in unique_ordered_label_pairs:
            # every pair must be "4"
            atom_site_pair_dict[pair] = "4"

    return atom_site_pair_dict

    # Generate all pairs

