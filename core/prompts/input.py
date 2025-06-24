import click


def prompt_to_include_nested_files() -> bool:
    """Prompt the user to decide whether to include nested .cif files in
    each folder."""
    click.echo(
        "\nWould you like to include nested .cif files in each folder above?"
    )
    add_nested_files = click.confirm("(Default: Y)", default=True)
    return add_nested_files


def prompt_to_use_CN_bond_fractions() -> bool:
    """Prompt the user to decide whether to use bond fractions in
    coordination number geometry."""
    click.echo(
        "\nWould like to use bond fractions in coordination number geometry?"
        " (for .png only)"
    )
    is_CN_used = click.confirm("(Default: N)", default=False)
    return is_CN_used


def prompt_to_use_existing_json_file() -> bool:
    """Prompt the user to decide whether to use an existing
    site_pairs.json file if available."""
    click.echo(
        "\nWould you like to use existing site_pairs.json if available?"
    )
    is_CN_used = click.confirm("(Default: Y)", default=True)
    return is_CN_used
