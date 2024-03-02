import gemmi
import re
from util.string_parser import remove_string_braket
from util.unit import get_radians_from_degrees
 
 
def get_atom_type(label):
    """
    print(get_atom_type("Co4(2)"))  # Output: "Co"
    print(get_atom_type("FeIII"))  # Output: "Fe"
    print(get_atom_type("Fe(III)"))  # Output: "Fe"
    print(get_atom_type("Mg12"))  # Output: "Mg"
    print(get_atom_type("OI"))  # Output: "O"
    print(get_atom_type("O3"))  # Output: "O"
    print(get_atom_type("Co2"))  # Output: "O"
    print(get_atom_type("Fe12k"))  # Output: "Fe"
    print(get_atom_type("Rh3A"))  # Output: "Rh"
    print(get_atom_type("Si3B"))  # Output: "Si"
    """
    # Splitting the label into separate parts if it contains parentheses
    parts = re.split(r'[()]', label)
    for part in parts:
        # Attempt to extract the atom type
        match = re.search(r'([A-Z][a-z]*)', part)
        if match:
            return match.group(1)
    return None


def get_loop_tags():
    """
    Returns a list of predefined loop tags commonly used for atomic site description.
    """
    loop_tags = ["_atom_site_label", "_atom_site_type_symbol",
            "_atom_site_symmetry_multiplicity", "_atom_site_Wyckoff_symbol",
            "_atom_site_fract_x", "_atom_site_fract_y","_atom_site_fract_z", "_atom_site_occupancy"]
    
    return loop_tags


def get_unit_cell_lengths_angles(block):
    """
    Returns the unit cell lengths and angles from a given block.
    """
    keys_lengths = ['_cell_length_a', '_cell_length_b', '_cell_length_c']
    keys_angles = ['_cell_angle_alpha', '_cell_angle_beta', '_cell_angle_gamma']

    lengths = [remove_string_braket(block.find_value(key)) for key in keys_lengths]
    angles = [remove_string_braket(block.find_value(key)) for key in keys_angles]

    return tuple(lengths + angles)


def get_CIF_block(filename):
    """
    Returns a CIF block from its CIF filename.
    """
    doc = gemmi.cif.read_file(filename)
    block = doc.sole_block()

    return block


def get_loop_values(block, loop_tags):
    """
    Retrieves loop values from a block for the specified tags.
    """
    loop_values = [block.find_loop(tag) for tag in loop_tags]

    # Check for zero or missing coordinates
    if len(loop_values[4]) == 0 or len(loop_values[5]) == 0 or len(loop_values[6]) == 0:  # missing coordinates
        raise RuntimeError("Missing atomic coordinates")

    return loop_values


def get_cell_lenghts_angles_rad(CIF_block):
    """
    Processes the CIF block data to retrieve cell dimensions and angles.
    """
    # Extract cell dimensions and angles from CIF block
    cell_lengths_angles = get_unit_cell_lengths_angles(CIF_block)
    cell_length_a, cell_length_b, cell_length_c, alpha_deg, beta_deg, gamma_deg = cell_lengths_angles
    
    # Convert angles from degrees to radians
    alpha_rad, beta_rad, gamma_rad = get_radians_from_degrees([alpha_deg, beta_deg, gamma_deg])

    # Store angles in radians and cell lengths in a list
    cell_angles_rad = [alpha_rad, beta_rad, gamma_rad]
    cell_lengths = [cell_length_a, cell_length_b, cell_length_c]

    return cell_lengths, cell_angles_rad
