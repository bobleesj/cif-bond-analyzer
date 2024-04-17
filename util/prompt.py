import textwrap
import click
from click import style, echo
from util import folder
import json


def print_intro_prompt():
    """Filters and moves CIF files based on the shortest atomic distance."""
    intro_prompt = textwrap.dedent(
        """\
    ===
    Welcome to the CIF Bond Analyzer!
                                   
    [1] Processes Crystallographic Information Files from selected folder.
    [2] Forms supercell.
    [3] Determines shortest unique atomic pairs found across all CIF files.
    [4] Indicates frequency and distances of bonding pairs.
    [5] Identifies missing atomic pairs not observed across all CIF files.
    [6] Generates histograms for each unique atomic pair.
                                    
    Let's get started!
    ===
    """
    )
    print(intro_prompt)


def get_folder_indices(dir_names_with_cif):
    while True:
        folder_numbers_str = click.prompt(
            "Enter the numbers corresponding to the folders listed above, separated by spaces. Ex) 1 2 3"
        )
        try:
            # Split the input by spaces, convert to integers, and filter out duplicates
            folder_indices = list(
                set(int(number) for number in folder_numbers_str.split())
            )

            # Check if all entered indices are valid
            if not all(
                1 <= idx <= len(dir_names_with_cif) for idx in folder_indices
            ):
                raise ValueError(
                    "One or more numbers are out of the valid range."
                )

            # Map the indices to directory names
            selected_dirs = {
                idx: dir_names_with_cif[idx - 1] for idx in folder_indices
            }
            return selected_dirs

        except ValueError:
            click.echo(
                "Please enter only valid numbers within the range, separated by spaces."
            )


def get_user_input_folder_processing(dir_names, file_type):
    click.echo(f"\nFolders with {file_type} files:")
    for idx, dir_name in enumerate(dir_names, start=1):
        num_of_cif_files = folder.get_cif_file_count_from_directory(dir_name)
        click.echo(f"{idx}. {dir_name}, {num_of_cif_files} files")

    click.echo("\nWould you like to process each folder above sequentially?")
    is_sequentially_processed = click.confirm("(Default: Y)", default=True)

    if is_sequentially_processed:
        selected_dirs = {
            idx: name for idx, name in enumerate(dir_names, start=1)
        }
    else:
        selected_dirs = get_folder_indices(dir_names)

    # Print the selected folders
    if len(selected_dirs) == len(dir_names):
        click.echo("> Good! Let's process all the folders.")
    else:
        click.echo("> Good! You've chosen the following folders:")
        for idx, dir_name in selected_dirs.items():
            click.echo(f"{idx}. {dir_name}")

    return selected_dirs


def get_user_input_on_supercell_method():
    echo(
        "\nWould you like to modify the default 2x2x2 supercell generation"
        " method for files over 100 atoms in the unit cell?"
    )
    is_supercell_generation_method_modified = click.confirm(
        "(Default: N)", default=False
    )

    if is_supercell_generation_method_modified:
        echo("\nChoose a supercell generation method:")
        echo("1. No shift (fastest)")
        echo("2. +1 +1 +1 shifts in x, y, z directions")
        echo("3. +-1, +-1, +-1 shifts (2x2x2 supercell generation, slowest)")

        method = click.prompt(
            "Choose your option by entering a number", type=int
        )

        if method == 1:
            echo("> You've selected: No shift (fastest)\n")
        elif method == 2:
            echo("> You've selected: +1 +1 +1 shifts in x, y, z directions\n")
        elif method == 3:
            echo(
                "> You've selected: +-1, +-1, +-1 shifts (2x2x2 supercell, slowest)\n"
            )
        else:
            echo("> Invalid option. Defaulting to No shift (fastest)\n")
            method = 1
    else:
        method = None

    return method


def echo_folder_progress(idx, dir_name, num_selected_dirs):
    echo("\n")
    echo("=" * 50)  # Top line of '=' characters
    echo(f"Processing {dir_name} ({idx} out of {num_selected_dirs})")
    echo("=" * 50)  # Bottom line of '=' characters


def print_progress(filename_with_ext, num_of_atoms, elapsed_time, is_finished):
    if is_finished:
        echo(
            style(
                f"Processed {filename_with_ext} with {num_of_atoms} atoms in "
                f"{round(elapsed_time, 2)} s\n",
                fg="blue",
            )
        )


def print_dict_in_json(data):
    print(json.dumps(data, indent=4, sort_keys=True))
