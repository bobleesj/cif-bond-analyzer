import click


def prompt_to_include_nested_files():
    click.echo("\nWould you like to include nested .cif files?")
    add_nested_files = click.confirm("(Default: N)", default=False)
    return add_nested_files
