# -*- coding: utf-8 -*-

"""Console script for staple."""
import sys
import click


@click.command()
@click.argument('input_files', nargs=-1, type=click.Path(exists=True))
@click.argument('output_file', nargs=1, type=click.Path())
@click.option('--verbose/--no-verbose', default=False)
@click.option('--binarize/--probabilities', default=True)
@click.option('--convergence-threshold')
def main(input_files, output_file, verbose, binarize, convergence_threshold):
    """Run STAPLE algorithm on a set of binary expert segmentations."""
    from staple import run_staple
    run_staple(
        input_files,
        output_file,
        verbose,
        binarize,
        convergence_threshold,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
