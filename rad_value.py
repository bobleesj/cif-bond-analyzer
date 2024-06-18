import pandas as pd


rad_data = {
    "Si": [1.176, 1.316],
    "Sc": [1.641, 1.620],
    "Fe": [1.242, 1.260],
    "Co": [1.250, 1.252],
    "Ni": [1.246, 1.244],
    "Ga": [1.243, 1.408],
    "Ge": [1.225, 1.366],
    "Y": [1.783, 1.797],
    "Ru": [1.324, 1.336],
    "Rh": [1.345, 1.342],
    "Pd": [1.376, 1.373],
    "In": [1.624, 1.660],
    "Sn": [1.511, 1.620],
    "Sb": [1.434, 1.590],
    "La": [1.871, 1.871],
    "Ce": [1.819, 1.818],
    "Pr": [1.820, 1.824],
    "Nd": [1.813, 1.818],
    "Sm": [1.793, 1.850],
    "Eu": [1.987, 2.084],
    "Gd": [1.787, 1.795],
    "Tb": [1.764, 1.773],
    "Dy": [1.752, 1.770],
    "Ho": [1.745, 1.761],
    "Er": [1.734, 1.748],
    "Tm": [1.726, 1.743],
    "Yb": [1.939, 1.933],
    "Lu": [1.718, 1.738],
    "Os": [1.337, 1.350],
    "Ir": [1.356, 1.355],
    "Pt": [1.387, 1.385],
    "Th": [1.798, 1.795],
    "U": [1.377, 1.51],
    "Al": [1.310, 1.310],
    "Mo": [1.362, 1.386],
    "Hf": [1.5635, 1.585],
    "Ta": [1.430, 1.457],
}


# Prepare a list to hold all data
data_for_excel = []

# Convert the dictionary to a list of dictionaries suitable for DataFrame
for element, values in rad_data.items():
    data_for_excel.append(
        {
            "Element": element,
            "First Value": values[0],
            "Second Value": values[1],
        }
    )

# Create a DataFrame
df = pd.DataFrame(data_for_excel)

# Define the Excel file name
excel_file_name = "element_values.xlsx"

# Write the DataFrame to an Excel file
df.to_excel(excel_file_name, index=False, engine="openpyxl")

print(f"Data successfully written to {excel_file_name}")
