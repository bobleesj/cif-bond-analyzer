import textwrap
import click

def print_intro_prompt():
    """Filters and moves CIF files based on the shortest atomic distance."""
    intro_prompt = textwrap.dedent("""\
    ===
    Welcome to the CIF Bond Analyzer!
    - Get the shortest and unique distances for each CIF file.
    - Save a histogra
                                   
    Let's get started!
    ===
    """)
    print(intro_prompt)


def get_user_input_on_file_skip():
    click.echo("Do you want to skip any CIF files based on the number of unique atoms in the supercell?")
    skip_based_on_atoms = click.confirm('(Default: N)', default=False)
    print()

    if skip_based_on_atoms:
        click.echo("Enter the threshold for the maximum number of atoms in the supercell.")
        supercell_max_atom_count = click.prompt('Files with atoms exceeding this count will be skipped\n', type=int)
    else:
        supercell_max_atom_count = float('inf')  # A large number to essentially disable skipping
    return supercell_max_atom_count
