import preprocess.cif_parser as cif_parser


def get_atom_info(CIF_loop_values, i):
    label = CIF_loop_values[0][i]
    occupancy = float(cif_parser.remove_string_braket(CIF_loop_values[7][i]))
    coordinates = (cif_parser.remove_string_braket(CIF_loop_values[4][i]),
                   cif_parser.remove_string_braket(CIF_loop_values[5][i]),
                   cif_parser.remove_string_braket(CIF_loop_values[6][i]))
    return label, occupancy, coordinates


def get_atom_site_mixing_info(filename, CIF_loop_values):
    num_atom_labels = len(CIF_loop_values[0])

    # Check for full occupancy
    coord_occupancy_sum = {}
    is_full_occupancy = True

    for i in range(num_atom_labels):
        label, occupancy, coordinates = get_atom_info(CIF_loop_values, i)
        occupancy_num = coord_occupancy_sum.get(coordinates, 0) + occupancy
        coord_occupancy_sum[coordinates] = occupancy_num

    #     print("label", label)
    #     print("occupancy", occupancy)

    # print("coord_occupancy_sum", coord_occupancy_sum)
    # Now check summed occupancies
    for coordinates, sum_occ in coord_occupancy_sum.items():
        if sum_occ != 1:
            is_full_occupancy = False
            print(f"Summed occupancy at {coordinates}: {sum_occ}")
            break

    # Check for atomic mixing
    is_atomic_mixing = len(coord_occupancy_sum) != num_atom_labels

    if is_atomic_mixing and not is_full_occupancy:
        print(filename, "has deficiency_atomic_mixing")

    elif is_atomic_mixing and is_full_occupancy:
        print(filename, "has full_occupancy_atomic_mixing")

    elif not is_atomic_mixing and not is_full_occupancy:
        print(filename, "has deficiency_no_atomic_mixing")

    elif is_full_occupancy:
        print(filename, "has full_occupancy")
