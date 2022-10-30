"""Console script for scrapemove."""

import sys

import click

from scrapemove.scrapemove import request


@click.command()
@click.argument('url')
@click.option('--parallelism', type=int)
def main(url, parallelism):
    """Console script for scrapemove."""
    click.echo(request(url, parallelism=parallelism))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
