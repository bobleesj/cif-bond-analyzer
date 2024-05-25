import re
import gemmi
from util.string_parser import remove_string_braket
from preprocess import cif_parser
from util.unit import get_radians_from_degrees


def get_atom_type(label):
    """
    Returns the element from the given label
    """
    parts = re.split(r"[()]", label)
    for part in parts:
        # Attempt to extract the atom type
        match = re.search(r"([A-Z][a-z]*)", part)
        if match:
            return match.group(1)
    return None


def get_loop_tags():
    """
    Returns tags commonly used for atomic description.
    """
    loop_tags = [
        "_atom_site_label",
        "_atom_site_type_symbol",
        "_atom_site_symmetry_multiplicity",
        "_atom_site_Wyckoff_symbol",
        "_atom_site_fract_x",
        "_atom_site_fract_y",
        "_atom_site_fract_z",
        "_atom_site_occupancy",
    ]

    return loop_tags


def get_unit_cell_lengths_angles(block):
    """
    Returns the unit cell lengths and angles from a given block.
    """
    keys_lengths = [
        "_cell_length_a",
        "_cell_length_b",
        "_cell_length_c",
    ]
    keys_angles = [
        "_cell_angle_alpha",
        "_cell_angle_beta",
        "_cell_angle_gamma",
    ]

    lengths = [
        remove_string_braket(block.find_value(key)) for key in keys_lengths
    ]
    angles = [
        remove_string_braket(block.find_value(key)) for key in keys_angles
    ]

    return tuple(lengths + angles)


def get_cif_block(file_path):
    """
    Returns CIF block from file path given.
    """
    doc = gemmi.cif.read_file(file_path)
    block = doc.sole_block()

    return block


def get_loop_values(block, loop_tags):
    """
    Retrieve a list of predefined loop tags for atomic site description.
    """

    loop_values = [block.find_loop(tag) for tag in loop_tags]

    # Check for zero or missing coordinates
    if (
        len(loop_values[4]) == 0
        or len(loop_values[5]) == 0
        or len(loop_values[6]) == 0
    ):
        raise RuntimeError("Missing atomic coordinates")

    return loop_values


def get_cell_lenghts_angles_rad(CIF_block):
    """
    Processes CIF block to retrieve cell dimensions and angles.
    """
    # Extract cell dimensions and angles from CIF block
    cell_lengths_angles = get_unit_cell_lengths_angles(CIF_block)
    (
        cell_len_a,
        cell_len_b,
        cell_len_c,
        alpha_deg,
        beta_deg,
        gamma_deg,
    ) = cell_lengths_angles

    # Convert angles from degrees to radians
    alpha_rad, beta_rad, gamma_rad = get_radians_from_degrees(
        [alpha_deg, beta_deg, gamma_deg]
    )

    # Store angles in radians and cell lengths in a list
    cell_angles_rad = [alpha_rad, beta_rad, gamma_rad]
    cell_lengths = [cell_len_a, cell_len_b, cell_len_c]

    return cell_lengths, cell_angles_rad


def get_num_of_atom_labels(cif_loop_values):
    """
    Count the number of labels in the loop.
    """
    return len(cif_loop_values[0])


def get_unique_element_list(cif_loop_values):
    """
    Get a list of unique elements from loop values.
    """
    num_atom_labels = get_num_of_atom_labels(cif_loop_values)
    element_list = []
    for i in range(num_atom_labels):
        element = cif_loop_values[1][i]
        element_list.append(element)
    return list(set(element_list))


def get_atom_label_list(cif_loop_values):
    """
    Get a list of atom labels from loop values.
    """
    num_atom_labels = get_num_of_atom_labels(cif_loop_values)
    label_list = []
    for i in range(num_atom_labels):
        element = cif_loop_values[0][i]
        label_list.append(element)

    return label_list


def get_atom_info(cif_loop_values, i):
    """
    Get atom information (label, occupancy, coordinates) for the i-th atom.
    """
    label = cif_loop_values[0][i]
    occupancy = float(remove_string_braket(cif_loop_values[7][i]))
    coordinates = (
        remove_string_braket(cif_loop_values[4][i]),
        remove_string_braket(cif_loop_values[5][i]),
        remove_string_braket(cif_loop_values[6][i]),
    )

    return label, occupancy, coordinates


def get_cif_loop_value_dict(ci_loop_values):
    """
    Create a dictionary containing CIF loop values organized by atom label.
    """
    cif_loop_value_dict = {}
    num_of_atom_labels = get_num_of_atom_labels(ci_loop_values)

    for i in range(num_of_atom_labels):
        label, occupancy, coordinates = get_atom_info(ci_loop_values, i)
        cif_loop_value_dict[label] = {}
        cif_loop_value_dict[label]["occupancy"] = occupancy
        cif_loop_value_dict[label]["coordinates"] = coordinates

    return cif_loop_value_dict


# Index is one lower than the actual line number
def get_line_start_end_line_indexes(file_path, start_keyword):
    """
    Finds the starting and ending indexes of the lines in atom_site_loop
    """

    with open(file_path, "r") as f:
        lines = f.readlines()

    start_index = None
    end_index = None

    # Find the start index
    for i, line in enumerate(lines):
        if start_keyword in line:
            start_index = i + 1
            break

    if start_index is None:
        return None, None

    # Find the end index
    for i in range(start_index, len(lines)):
        if lines[i].strip() == "":
            end_index = i
            break

    return start_index, end_index


def get_loop_content(file_path, start_keyword):
    start_index, end_index = get_line_start_end_line_indexes(
        file_path, start_keyword
    )

    if start_index is None or end_index is None:
        print("Section starting with", start_keyword, "not found.")
        return None

    with open(file_path, "r") as f:
        lines = f.readlines()

    # Extract the content between start_index and end_index
    content_lines = lines[start_index:end_index]

    return content_lines


def extract_formula_and_tag(compound_formula_tag):
    parts = compound_formula_tag.split()

    # First part is the compound formula
    compound_formula = parts[0]

    # The rest are tags
    tags = "_".join(parts[1:])

    return compound_formula, tags


def get_compound_phase_tag_id_from_third_line(file_path):
    """
    Extracts the compound name and tag from the provided CIF file path.
    """
    with open(file_path, "r") as f:
        # Read first three lines
        f.readline()  # First line
        f.readline()  # Second line
        third_line = f.readline().strip()  # Thrid line
        third_line = third_line.replace(",", "")

        # Split based on '#' and filter out empty strings
        third_line_parts = [
            part.strip() for part in third_line.split("#") if part.strip()
        ]
        CIF_id = third_line_parts[-1]
        if not CIF_id.isdigit():
            raise RuntimeError(
                "The CIF file is wrongly formatted in the third line"
            )

        # If the thrid line does not contain the CIF ID, then it's wrongly formatted
        # if third_line_parts[0] not in third_line_parts[1]

        compound_phase = third_line_parts[0]
        compound_formala_tag = third_line_parts[1]
        compound_id = third_line_parts[2]

        compound_formula, tags = extract_formula_and_tag(compound_formala_tag)
        return compound_phase, compound_formula, tags, compound_id
