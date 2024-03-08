import pandas as pd
import preprocess.cif_parser as cif_parser


def get_mendeleev_num_from_tuple(pair_tuple):
    # Parse the first and second elements
    first_element = cif_parser.get_atom_type(pair_tuple[0])
    second_element = cif_parser.get_atom_type(pair_tuple[1])
    
    # Read Excel
    df = pd.read_excel("element_Mendeleev_numbers.xlsx")
    
    # Get Mendeleev number for the first element
    first_mendeleev_num = (
        df.loc[df['Symbol'] == first_element, 'Mendeleev number'].iloc[0]
    )

    # Get Mendeleev number for the second element
    second_mendeleev_num = (
        df.loc[df['Symbol'] == second_element, 'Mendeleev number'].iloc[0]
    )

    return first_mendeleev_num, second_mendeleev_num


def order_pair_based_on_mendeleev_num(pair_tuple):
    first_element = pair_tuple[0]
    second_element = pair_tuple[1]

    first_mendeleev_num, second_mendeleev_num = get_mendeleev_num_from_tuple(
        pair_tuple
    )

    # First element num must be smaller
    if first_mendeleev_num > second_mendeleev_num:
        return (second_element, first_element)

    else:
        return (first_element, second_element)


# Get True or False whether the pair is ordered
def is_pair_ordered_by_mendeleev(pair_tuple):
    first_mendeleev_num, second_mendeleev_num = get_mendeleev_num_from_tuple(
        pair_tuple
    )

    # First element num must be smaller
    if first_mendeleev_num > second_mendeleev_num:
        return False

    else:
        return True


def sort_tuple_in_list(tuple_list):
    return [tuple(sorted(item)) for item in tuple_list]
