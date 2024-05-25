from postprocess.system import system_util
from util import prompt


def get_structure_dict(
    unique_structure_types,
    possible_bond_pairs,
    updated_json_file_path,
):
    structure_dict = system_util.init_structure_dict(
        unique_structure_types, possible_bond_pairs
    )

    # Add files and formulas
    structure_dict = system_util.add_files_and_formula(
        structure_dict, updated_json_file_path
    )

    # Add bond lenghts and bond statistics
    structure_dict = system_util.add_bond_lenghts_and_statistics(
        structure_dict, updated_json_file_path
    )

    # Add unique bond counts
    structure_dict = system_util.add_unique_bond_count_per_bond_type(
        structure_dict
    )

    # Add bond fractions
    structure_dict = system_util.add_bond_fractions_per_structure(
        structure_dict
    )

    return structure_dict
