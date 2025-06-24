from click import echo, style


def prompt_folder_progress(i, dir_name, dirs_total_count):
    """Display a progress header for folder processing with boundaries
    and folder information."""
    count = 70
    echo("\n")
    echo("=" * count)  # Top line of '=' characters
    echo(f"Processing {dir_name}, ({i} out of {dirs_total_count})")
    echo("=" * count)  # Bottom line of '=' characters


def prompt_progress_current(i, filename, supercell_atom_count, file_count):
    """Display the current progress for processing a file, highlighting
    the filename, atom count, and its order in the sequence."""
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
    """Display a completion message for a file, showing the filename,
    atom count, and the elapsed time in seconds."""
    echo(
        style(
            f"Processed {filename} with {supercell_atom_count} atoms in "
            f"{round(elapsed_time, 2)} s\n",
            fg="blue",
        )
    )


def prompt_file_saved(file_path):
    """Display a file has been saved."""
    echo(
        style(
            f"Saved {file_path}",
            fg="blue",
        )
    )
