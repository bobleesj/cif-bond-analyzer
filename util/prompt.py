import textwrap
import click
import logging
from click import style, echo
from util import folder
import json


def prompt_site_analysis_intro():
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
            "Enter the numbers corresponding to the folders listed above,"
            " separated by spaces. Ex) 1 2 3"
        )
        try:
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


def echo_folder_progress(idx, dir_name, num_selected_dirs):
    echo("\n")
    echo("=" * 50)  # Top line of '=' characters
    echo(f"Processing {dir_name} ({idx} out of {num_selected_dirs})")
    echo("=" * 50)  # Bottom line of '=' characters


def print_progress_finished(
    filename_with_ext, num_of_atoms, elapsed_time, is_finished
):
    if is_finished:
        echo(
            style(
                f"Processed {filename_with_ext} with {num_of_atoms} atoms in "
                f"{round(elapsed_time, 2)} s\n",
                fg="blue",
            )
        )


def print_progress_current(
    i, filename_with_ext, supercell_points, num_of_files
):
    echo(
        style(
            f"Processing {filename_with_ext} with "
            f"{len(supercell_points)} atoms ({i+1}/{num_of_files})",
            fg="yellow",
        )
    )


def print_dict_in_json(data):
    print(json.dumps(data, indent=4, sort_keys=True))


def prompt_system_analysis_intro():
    echo(
        "\nNote: All of the .cif files must be either binary or ternary files"
        " or combined. Only up to 3 unique elements are allowed."
        " If the shortest distance from each site is NOT calculated with option [1],"
        " the program will run option [1] automatically. Also, if there is a new .cif"
        " added to the folder, it will run option [1] again."
    )
