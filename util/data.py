import pandas as pd


def get_mendeleev_numbers(data):
    data = "data/element_Mendeleev_numbers.xlsx"
    df = pd.read_excel(data, header=None)
    elements = df.iloc[
        :, 0
    ]  # Assuming elements are in the first column
    mendeleev_numbers = df.iloc[
        :, 1
    ]  # Assuming Mendeleev numbers are in the 6th column
    return dict(zip(elements, mendeleev_numbers))
