import pandas as pd


def order_pair_based_on_mendeleev_num(pair_tuple):
    
    # Parse the first and second elements
    first_element = pair_tuple[0]
    second_element = pair_tuple[1]
    
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
    # Sort the tuple based on this

    if second_mendeleev_num < first_mendeleev_num:
        return (second_element, first_element)
    
    return (first_element, second_element)
    

    

    
