# def draw_horizontal_line_with_marks(bond_fractions_list, bond_types):
#     fig, ax = plt.subplots()  # Create a figure and an axes.

#     # Draw the horizontal line
#     ax.plot(
#         [0, 1], [0, 0], "k-", lw=2
#     )  # Single line for both markers

#     # Add labels at the ends of the line
#     ax.text(
#         0,
#         0,
#         "Co",
#         fontsize=12,
#         ha="right",
#         va="center",
#         backgroundcolor="white",
#     )
#     ax.text(
#         1,
#         0,
#         "In",
#         fontsize=12,
#         ha="left",
#         va="center",
#         backgroundcolor="white",
#     )

#     my_parsed_formulas = []
#     # Place marks along the line
#     for bond_fractions in bond_fractions_list:
#         form = bond_fractions[0]
#         normalized_formula = formula_parser.get_normalized_formula(
#             labels
#         )
#         parsed_normalized_formula = formula_parser.get_parsed_formula(
#             normalized_formula
#         )
#         my_parsed_formulas.append((labels, parsed_normalized_formula))

#     for formula, labels in my_parsed_formulas:
#         # Find the position for 'In' from the formula and place a marker
#         for element, fraction_str in labels:
#             fraction = float(fraction_str)
#             if element == "In":
#                 ax.plot(
#                     fraction,
#                     0,
#                     "ro",
#                     label=f"{formula}",
#                 )  # Place marker at the fraction
#                 ax.text(
#                     fraction,
#                     0.05,
#                     f"{formula}",
#                     fontsize=7,
#                     ha="center",
#                     va="bottom",
#                 )

#     # Set limits to slightly beyond the ends to ensure visibility of labels and markers
#     ax.set_xlim(-0.1, 1.1)
#     ax.set_ylim(-0.2, 0.2)

#     # Remove axes and ticks
#     ax.axis("off")

#     # Show the plot
#     plt.show()
