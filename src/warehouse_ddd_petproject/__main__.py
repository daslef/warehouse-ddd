"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Warehouse Ddd."""


if __name__ == "__main__":
    main(prog_name="warehouse-ddd")  # pragma: no cover
