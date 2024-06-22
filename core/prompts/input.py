import click


def prompt_to_include_nested_files():
    click.echo(
        "\nWould you like to include nested .cif files in each folder above?"
    )
    add_nested_files = click.confirm("(Default: N)", default=False)
    return add_nested_files


def prompt_to_use_CN_bond_fractions():
    click.echo(
        "\nWould like to use bond fractions in coordination number geometry?"
    )
    is_CN_used = click.confirm("(Default: N)", default=False)
    return is_CN_used


def prompt_to_use_existing_json_file():
    click.echo(
        "\nWould you like to use existing site_pairs.json if available?"
    )
    is_CN_used = click.confirm("(Default: Y)", default=True)
    return is_CN_used
