import gemmi
import re
from util.string_parser import remove_string_braket
from util.unit import get_radians_from_degrees

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
    with open(file_path, 'r') as f:
        # Read first three lines
        f.readline() # First line
        f.readline() # Second line
        third_line = f.readline().strip() # Thrid line
        third_line = third_line.replace(",", "")
        
        # Split based on '#' and filter out empty strings
        third_line_parts = [part.strip() for part in third_line.split("#") if part.strip()]
        CIF_id =  third_line_parts[-1]
        if not CIF_id.isdigit():
            raise RuntimeError("The CIF file is wrongly formatted in the third line")
                
        
        # If the thrid line does not contain the CIF ID, then it's wrongly formatted
        # if third_line_parts[0] not in third_line_parts[1]

        compound_phase = third_line_parts[0]
        compound_formala_tag = third_line_parts[1]
        compound_id = third_line_parts[2]

        compound_formula, tags = extract_formula_and_tag(compound_formala_tag)
        return compound_phase, compound_formula, tags, compound_id


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


def extract_formula_and_atoms(block):
    """
    Extract the chemical formula and unique atoms from a CIF block.
    """

    A_labels = ["Sc", "Y", "La", "Ce", "Pr", "Nd", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Th", "U"]
    B_labels = ["Si", "Ga", "Ge", "In", "Sn", "Sb"]
    M_labels = ["Fe", "Co", "Ni", "Ru", "Rh", "Pd", "Os", "Ir", "Pt"]
    
    formula = None
    formula_string = None

    if block.find_pair('_chemical_formula_structural'):
        formula = block.find_pair('_chemical_formula_structural')
    elif block.find_pair('_chemical_formula_sum'):
        formula = block.find_pair('_chemical_formula_sum')
    
    if formula:
        formula_string = formula[1]
        formula_string = formula_string.replace("'", "")
        formula_string = re.sub('[~ ]', '', formula_string)

    if not formula_string:
        return None, 0, None

    pattern = re.compile(r"([A-Z][a-z]*)(\d*)")
    matches = pattern.findall(formula_string)
    unique_atoms_tuple = [(atom, int(count) if count else 1) for atom, count in matches]
    num_of_unique_atoms = len({atom for atom, _ in unique_atoms_tuple})
    sorted_unique_atoms_tuple = None

    A_elements = []
    B_elements = []
    M_elements = []

    for atom, count in unique_atoms_tuple:
        if atom in A_labels:
            A_elements.append((atom, count))
        elif atom in B_labels:
            B_elements.append((atom, count))
        elif atom in M_labels:
            M_elements.append((atom, count))


    # Binary system
    if num_of_unique_atoms == 2:
        if len(A_elements) == 0 and len(B_elements) == 0:
            sorted_unique_atoms_tuple = unique_atoms_tuple
        elif len(A_elements) == 0 and len(B_elements) == 1:
            A_elements = [(atom, count) for atom, count in unique_atoms_tuple if atom not in B_labels]
        elif len(B_elements) == 0 and len(A_elements) == 1:
            B_elements = [(atom, count) for atom, count in unique_atoms_tuple if atom not in A_labels]
        
        if len(A_elements) != 0 or len(B_elements) != 0:
            sorted_unique_atoms_tuple = A_elements + B_elements

    # Ternary system
    if num_of_unique_atoms == 3:
        if len(A_elements) == 0 and len(B_elements) == 0 and len(M_elements) == 0:
            sorted_unique_atoms_tuple = unique_atoms_tuple
        elif len(A_elements) == 1 and len(B_elements) == 1:
            # One atom each in A and B: the remaining one should be M
            M_elements = [(atom, count) for atom, count in unique_atoms_tuple if atom not in A_labels and atom not in B_labels]
        elif len(A_elements) == 0 and len(B_elements) == 1:
            # One atom in B: the remaining ones should be A and M
            M_elements = [(atom, count) for atom, count in unique_atoms_tuple if atom not in B_labels]
            A_elements = [(atom, count) for atom, count in unique_atoms_tuple if atom not in B_labels and atom not in M_labels]
        elif len(A_elements) == 1 and len(B_elements) == 0:
            # One atom in A: the remaining ones should be B and M
            M_elements = [(atom, count) for atom, count in unique_atoms_tuple if atom not in A_labels]
            B_elements = [(atom, count) for atom, count in unique_atoms_tuple if atom not in A_labels and atom not in M_labels]
        elif len(A_elements) == 1 and len(M_elements) == 1:
            # One atom in A and one in M: the remaining one should be B
            B_elements = [(atom, count) for atom, count in unique_atoms_tuple if atom not in A_labels and atom not in M_labels]
        elif len(B_elements) == 1 and len(M_elements) == 1:
            # One atom in B and one in M: the remaining one should be A
            A_elements = [(atom, count) for atom, count in unique_atoms_tuple if atom not in B_labels and atom not in M_labels]
        elif len(A_elements) == 0 and len(M_elements) == 1:
            # One atom in M: the remaining ones should be A and B
            A_elements = [(atom, count) for atom, count in unique_atoms_tuple if atom not in B_labels and atom not in M_labels]
            B_elements = [(atom, count) for atom, count in unique_atoms_tuple if atom not in A_labels and atom not in M_labels]
        
        if len(A_elements) != 0 or len(B_elements) != 0 or len(M_elements) != 0:
            sorted_unique_atoms_tuple = A_elements + M_elements + B_elements

    return sorted_unique_atoms_tuple, num_of_unique_atoms, formula_string


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