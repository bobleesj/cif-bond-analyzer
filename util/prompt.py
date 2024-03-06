import textwrap
import click

def print_intro_prompt():
    """Filters and moves CIF files based on the shortest atomic distance."""
    intro_prompt = textwrap.dedent("""\
    ===
    Welcome to the CIF Bond Analyzer!
                                   
    What this script does
    [1] Processes Crystallographic Information Files from selected folder.
    [2] Forms supercell based CIF info.
    [3] Determines shortest unique atomic pairs found across all CIF files.
    [4] Indicates frequency and distances of bonding pairs.
    [5] Identifies missing atomic pairs not observed across all CIF files.
    [6] Generates histograms for each unique atomic pair
                                    
    Let's get started!
    ===
    """)
    print(intro_prompt)


def get_user_input_on_supercell_method():
    click.echo("\nDo you want to modify the supercell generation method for CIF files with more than 100 atoms in the unit cell?")
    is_supercell_generation_method_modified = click.confirm('(Default: N)', default=False)

    if is_supercell_generation_method_modified:
        click.echo("\nChoose a supercell generation method:")
        click.echo("1. No shift (fastest)")
        click.echo("2. +1 +1 +1 shifts in x, y, z directions")
        click.echo("3. +-1, +-1, +-1 shifts (2x2x2 supercell generation, requires heavy computation, slowest)")
        
        method = click.prompt("Choose your option by entering a number", type=int)
        
        if method == 1:
            click.echo("You've selected: No shift (fastest)\n")
        elif method == 2:
            click.echo("You've selected: +1 +1 +1 shifts in x, y, z directions\n")
        elif method == 3:
            click.echo("You've selected: +-1, +-1, +-1 shifts (2x2x2 supercell generation, slowest)\n")
        else:
            click.echo("Invalid option. Defaulting to No shift (fastest)\n")
            method = 1 
    else:
        method = None

    return method
