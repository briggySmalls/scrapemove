"""Console script for scrapemove."""

import sys

import click

from scrapemove.scrapemove import request


@click.command()
@click.argument("url")
@click.option("--parallelism", type=int)
@click.option("--details/--no-details", default=False)
def main(url, parallelism, details):
    """Console script for scrapemove."""
    click.echo(request(url, detailed=details, parallelism=parallelism))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
