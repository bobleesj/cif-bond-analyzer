import json
import os
import pandas as pd


def save_to_excel_json(all_labels_connections, output_folder, filename):
    """
    Saves the connection data for each label to an Excel file
    """
    # Save Excel
    excel_file_path = os.path.join(output_folder, filename + ".xlsx")
    # Create an Excel writer object using pandas
    with pd.ExcelWriter(excel_file_path, engine="openpyxl") as writer:
        for label, connections in all_labels_connections.items():
            if connections:
                # Convert the connection data into a DataFrame
                df = pd.DataFrame(
                    connections,
                    columns=[
                        "site_label",
                        "distance_angstrom",
                        "coord_1",
                        "coord_2",
                        "norm_diff",
                    ],
                )
                # df = df.drop(columns=["coord_1", "coord_2"])
                # Write the DataFrame to an Excel sheet named after the label
                df.to_excel(writer, sheet_name=label, index=False)
                print(f"Data for {label} saved to Excel sheet.")
            else:
                print(f"No data available for {label}, no sheet created.")

    # Save to JSON
    json_file_path = os.path.join(output_folder, filename + ".json")
    with open(json_file_path, "w") as json_file:
        json.dump(all_labels_connections, json_file, indent=4)
    print(f"Data saved to JSON file: {json_file_path}")


def save_text_file(
    all_labels_connections, output_folder, filename, is_CN_used
):
    """
    Saves the connection data for each label to an .txt file
    """
    text_file_path = os.path.join(output_folder, filename + ".txt")
    is_verbose_output = True

    # Define field widths
    label_width = 5
    dist_width = 7
    coord_width = 23
    norm_diff_width = 10

    if is_verbose_output:
        filename += "_v"

    text_file_path = os.path.join(output_folder, filename + ".txt")

    # Create the text file
    with open(text_file_path, "w") as text_file:
        for label, connections in all_labels_connections.items():
            top_label = (
                f"{label} CN:{len(connections)}"
                if is_CN_used
                else f"{label} count:{len(connections)}"
            )
            if connections:
                text_file.write(f"{top_label}\n")
                for connection in connections:
                    (
                        site_label,
                        distance,
                        coord_1,
                        coord_2,
                        norm_diff,
                    ) = connection

                    # Format coordinates and norm_diff to 3 decimal places
                    coord_1_str = ", ".join(f"{c:.3f}" for c in coord_1)
                    coord_2_str = ", ".join(f"{c:.3f}" for c in coord_2)
                    distance_str = f"{distance:.3f}"
                    norm_diff_str = (
                        f"{norm_diff:.3f}" if norm_diff is not None else ""
                    )

                    if is_verbose_output:
                        text_file.write(
                            f"{site_label:<{label_width}} dist: {distance_str:<{dist_width}} "
                            f"coord 1: {coord_1_str:<{coord_width}} coord 2: {coord_2_str:<{coord_width}} "
                            f"norm_diff: {norm_diff_str:<{norm_diff_width}}\n"
                        )
                    else:
                        text_file.write(
                            f"{site_label:<{label_width}} {distance_str:<{dist_width}}\n"
                        )
                text_file.write("\n")
            else:
                text_file.write(f"No data available for {label}\n\n")

    print(f"Data saved to text file: {text_file_path}")
