from preprocess import cif_parser
from util import formula_parser


def print_conneted_points(all_labels_connections):
    # Print all collected results
    print("All labels and their most connected points:")
    for label, connections in all_labels_connections.items():
        print(f"\nAtom site {label}:")
        for (
            label,
            dist,
            coords_1,
            coords_2,
        ) in connections:
            print(f"{label} {dist} {coords_1}, {coords_2}")
    print()


def get_pair_distances_dict_for_binary_ternary(
    all_labels_connections, formula
):
    num_of_unique_elements = formula_parser.get_num_element(formula)
    unique_pairs = get_flattend_pairs(all_labels_connections)
    min_dists = get_pairs_min_distances(unique_pairs)
    parsed_formula = formula_parser.get_parsed_formula(formula)

    if num_of_unique_elements == 2:
        A = parsed_formula[0][0]  # First element symbol
        B = parsed_formula[1][0]  # Second element symbol
        # Binary case: A-A, A-B, B-B
        AA_min = min_dists.get(tuple(sorted([A, A])), float("inf"))
        AB_min = min_dists.get(tuple(sorted([A, B])), float("inf"))
        BB_min = min_dists.get(tuple(sorted([B, B])), float("inf"))

        distances_dict = {"AA": AA_min, "AB": AB_min, "BB": BB_min}

    elif num_of_unique_elements == 3:
        # Ternary case: Assume the third element is C
        A = parsed_formula[0][0]  # First element symbol
        B = parsed_formula[1][0]  # Second element symbol
        C = parsed_formula[2][0]  # Third element symbol
        RR_min = min_dists.get(tuple(sorted([A, A])), float("inf"))
        RM_min = min_dists.get(tuple(sorted([A, B])), float("inf"))
        RX_min = min_dists.get(tuple(sorted([A, C])), float("inf"))
        MM_min = min_dists.get(tuple(sorted([B, B])), float("inf"))
        MX_min = min_dists.get(tuple(sorted([B, C])), float("inf"))
        XX_min = min_dists.get(tuple(sorted([C, C])), float("inf"))

        distances_dict = {
            "RR": RR_min,
            "MM": MM_min,
            "XX": XX_min,
            "RM": RM_min,
            "MX": MX_min,
            "RX": RX_min,
        }
    return distances_dict


def get_first_shortest_distances(distances_dict):
    """
    Extracts the shortest distance from each list of sorted distances
    in the provided dictionary.
    """
    shortest_distances = {}
    for pair, distances in distances_dict.items():
        # Access the first element of each list, which is the shortest distance
        shortest_distances[pair] = distances[0] if distances else float("inf")
    print(shortest_distances)
    return shortest_distances


def get_second_sortest_distances(distances_dict):
    """
    Extracts the shortest distance from each list of sorted distances
    in the provided dictionary.
    """
    shortest_distances = {}
    for pair, distances in distances_dict.items():
        # Access the first element of each list, which is the shortest distance
        shortest_distances[pair] = distances[1] if distances else float("inf")
    print(shortest_distances)
    return shortest_distances


def get_pairs_min_distances(pairs: set) -> dict:
    """
    Collects all distances for each unique pair of atom types from a set of pairs,
    and sorts them from shortest to longest.
    """

    distances_per_bond_pair = {}

    for ref_atom_type, other_atom_type, dist in pairs:
        # Sort the pair to avoid duplicate pairs in reverse order
        pair_key = tuple(sorted([ref_atom_type, other_atom_type]))

        # Append distance to the list of distances for the current pair
        if pair_key not in distances_per_bond_pair:
            distances_per_bond_pair[pair_key] = []
        distances_per_bond_pair[pair_key].append(dist)

    # Sort distances for each pair
    sorted_distances_per_bond_pair = {
        pair: sorted(distances)
        for pair, distances in distances_per_bond_pair.items()
    }

    return sorted_distances_per_bond_pair


def get_flattend_pairs(all_labels_connections: dict) -> set:
    unique_set = set()

    for label_type, connections in all_labels_connections.items():
        for connetion in connections:
            ref_atom_type = cif_parser.get_atom_type(label_type)
            other_atom_type = cif_parser.get_atom_type(connetion[0])
            dist = connetion[1]
            unique_set.add((ref_atom_type, other_atom_type, dist))
    return unique_set
