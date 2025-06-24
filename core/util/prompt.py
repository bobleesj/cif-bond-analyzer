import json

import click
from cifkit.utils import folder


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

    for i, dir_name in enumerate(dir_names, start=1):
        file_paths = folder.get_file_paths(dir_name, add_nested_files=False)
        file_paths_with_nested = folder.get_file_paths(
            dir_name, add_nested_files=True
        )
        nested_file_count = len(file_paths_with_nested) - len(file_paths)

        if nested_file_count != 0:
            click.echo(
                f"{i}. {dir_name}, {len(file_paths)} files, {nested_file_count} nested files"
            )
        else:
            click.echo(f"{i}. {dir_name}, {len(file_paths)} files")

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
        for i, dir_name in selected_dirs.items():
            click.echo(f"{i}. {dir_name}")

    return selected_dirs


def print_dict_in_json(data):
    print(json.dumps(data, indent=4, sort_keys=True))


def log_conneted_points(all_labels_connections):
    for (
        label,
        connections,
    ) in all_labels_connections.items():
        print(f"\nAtom site {label}:")
        for (
            label,
            dist,
            coords_1,
            coords_2,
        ) in connections:
            print(f"{label} {dist} {coords_1}, {coords_2}")
    print()
