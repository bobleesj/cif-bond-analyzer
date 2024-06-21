from click import style, echo


def prompt_folder_progress(i, dir_name, dirs_total_count, file_count=None):
    count = 70
    echo("\n")
    echo("=" * count)  # Top line of '=' characters
    echo(
        f"Processing {dir_name}, {file_count} files, ({i} out of {dirs_total_count})"
    )
    echo("=" * count)  # Bottom line of '=' characters


def prompt_progress_current(i, filename, supercell_atom_count, file_count):
    echo(
        style(
            f"Processing {filename} with "
            f"{supercell_atom_count} atoms ({i}/{file_count})",
            fg="yellow",
        )
    )


def prompt_progress_finished(
    filename,
    supercell_atom_count,
    elapsed_time,
):
    echo(
        style(
            f"Processed {filename} with {supercell_atom_count} atoms in "
            f"{round(elapsed_time, 2)} s\n",
            fg="blue",
        )
    )
