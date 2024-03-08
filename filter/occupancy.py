from itertools import product
import preprocess.cif_parser as cif_parser
import postprocess.pair_order as pair_order


def get_coord_occupancy_sum(CIF_loop_values):
    num_atom_labels = cif_parser.get_num_of_atom_labels(CIF_loop_values)
    # Check for full occupancy
    coord_occupancy_sum = {}

    for i in range(num_atom_labels):
        _, occupancy, coordinates = cif_parser.get_atom_info(
            CIF_loop_values, i
        )
        occupancy_num = coord_occupancy_sum.get(coordinates, 0) + occupancy
        coord_occupancy_sum[coordinates] = occupancy_num

    return coord_occupancy_sum


def get_atom_site_mixing_info(CIF_loop_values):
    is_full_occupancy = True

    coord_occupancy_sum = get_coord_occupancy_sum(CIF_loop_values)

    # Now check summed occupancies
    for coordinates, occupancy_sum in coord_occupancy_sum.items():
        if occupancy_sum != 1:
            is_full_occupancy = False

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
    
    # Step 1: Sort each pair to standardize order
    sorted_pairs = pair_order.sort_tuple_in_list(all_possible_label_pairs)

    # Step 2: Get only the unique pairs
    unique_sorted_pairs = list(set(sorted_pairs))

    # Step 3. Order pairs based on Mendeleev ordering
    unique_sorted_pairs_ordered = (
        [tuple(pair_order.order_pair_based_on_mendeleev_num(pair))
         for pair in unique_sorted_pairs]
    )

    return unique_sorted_pairs_ordered


# Get atom site mixing label for all pairs possible
def get_atom_site_mixing_dict(
        atom_site_mixing_file_info, CIF_loop_values):

    atom_site_pair_dict = {}
    unique_ordered_label_pairs = get_all_possible_ordered_label_pairs(
        CIF_loop_values
    )

    '''
    Step 1. Check full occupacny at the file level
    '''
    if atom_site_mixing_file_info == "4":
        for pair in unique_ordered_label_pairs:
            atom_site_pair_dict[pair] = "4"

    # Get label dict info and site occupancy sum
    cif_loop_value_dict = cif_parser.get_cif_loop_value_dict(CIF_loop_values)
    occupancy_sum = get_coord_occupancy_sum(CIF_loop_values)

    '''
    Step 2. If not, loop through every ordered label pair per file
    '''
    if atom_site_mixing_file_info != "4":
        for idx, pair in enumerate(unique_ordered_label_pairs):
            print("Label number:", idx+1)
            # Step 1: For the given pair, get the coordinate and occupany info
            first_label_coord = cif_loop_value_dict[pair[0]]["coordinates"]
            second_label_coord = cif_loop_value_dict[pair[1]]["coordinates"]

            first_label_occ = cif_loop_value_dict[pair[0]]["occupancy"]
            second_label_occ = cif_loop_value_dict[pair[1]]["occupancy"]

            print(
                "first_label:",
                pair[0],
                first_label_coord,
                first_label_occ
            )
            print(
                "second_label:",
                pair[1],
                second_label_coord,
                second_label_occ
            )

            '''
            Step 3. Check full occupacny at the pair level
            '''

            # Assign "4" for "full_occupancy"
            if first_label_occ == 1 and second_label_occ == 1:
                print("Both labels have full occupancy!",
                      "automatically set to 4\n")
                atom_site_pair_dict[pair] = "4"
                continue
    
            '''
            Step 4. Check deficiecny at the pair level
            '''
            # Check whehter one of the sites is deficient
            is_first_label_site_deficient = None
            is_second_label_deficient = None

            if first_label_occ < 1 or second_label_occ < 1:
                if occupancy_sum[first_label_coord] < 1:
                    is_first_label_site_deficient = True
                else:
                    is_first_label_site_deficient = False

                if occupancy_sum[second_label_coord] < 1:
                    is_second_label_deficient = True
                    
                else:
                    is_second_label_deficient = False

            '''
            Step 5. Check mixing at the pair level
            - Subtract current label coordinates occupancy from the sum,
            - If is zero, then no atomic mixing
            '''

            is_first_label_atomic_mixed = None
            is_second_label_atomic_mixed = None

            if (occupancy_sum[first_label_coord] - first_label_occ) == 0:
                is_first_label_atomic_mixed = False
            else:
                is_first_label_atomic_mixed = True

            if (occupancy_sum[second_label_coord] - second_label_occ) == 0:
                is_second_label_atomic_mixed = False
            else:
                is_second_label_atomic_mixed = True

            '''
            Step 6. Assign occupancy category for each label pair
            '''
            
            # Assign "3" for "deficiency_no_atomic_mixing"
            # Check 1. One of the labels is deficient
            # Check 2. Both labels are not atomic mixed
            if ((is_first_label_site_deficient or
                 is_second_label_deficient) and
                (not is_first_label_atomic_mixed and
                 not is_second_label_atomic_mixed)):
                atom_site_pair_dict[pair] = "3"

            # Assign "2" for "full_occupancy_atomic_mixing"
            # Check 1. Both labels are not deficient
            # Check 2. At least one label is atomic mixed
            if ((not is_first_label_site_deficient
                 and not is_second_label_deficient) and
                (is_first_label_atomic_mixed or
                 is_second_label_atomic_mixed)):
                atom_site_pair_dict[pair] = "2"

            # Assign "1" for "deficiency"
            # Check 1. At least one label is deficient
            # Check 2. At least one label mixed
            if ((is_first_label_site_deficient or
                 is_second_label_deficient) and
                (is_first_label_atomic_mixed or
                 is_second_label_atomic_mixed)):
                atom_site_pair_dict[pair] = "1"

            print()

    return atom_site_pair_dict
