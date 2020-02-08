# -*- coding: utf-8 -*-

import os
from contextlib import contextmanager
from pathlib import Path

import click
import pytest
import matplotlib.pyplot as plt

from . import constants
from .config import load_config
from .utils import make_data_directory
from .report import make_benchmark_report, plot_benchmark, get_benchmark_names


@contextmanager
def cd(path: Path):
    old_path = os.getcwd()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(old_path)


@click.group()
@click.option('-c', '--config', 'config_path', type=Path, default=None,
              help='Benchmark configuration YAML file')
def cli(config_path):
    load_config(config_path)


@cli.command(context_settings={'ignore_unknown_options': True})
@click.argument('pytest_args', nargs=-1, type=click.UNPROCESSED)
def run(pytest_args):
    """Run benchmarks
    """

    make_data_directory()

    args = [
        # pytest args
        str(constants.BENCHMARKS_PATH),
        '--rootdir', str(constants.PKG_PATH),
        '-c', str(constants.PYTEST_CONFIG_PATH),
        '-o', f'cache_dir={constants.PYTEST_CACHE_PATH.as_posix()}',
        '-v',

        # pytest-benchmark args
        '--benchmark-only',
        '--benchmark-autosave',
        '--benchmark-storage', str(constants.BENCHMARK_STORAGE_PATH),
        '--benchmark-columns', 'min,max,mean,median,stddev,rounds',
        '--benchmark-sort', 'mean',

        # Additional pytest/pytest-benchmark args
        *pytest_args,
    ]

    with cd(constants.BENCHMARKS_PATH):
        status_code = pytest.main(args)

    if status_code == 0:
        make_benchmark_report()

    return status_code


@cli.command()
def report():
    make_benchmark_report()


@cli.command()
@click.option('-i', '--id', 'ids', type=str, multiple=True,
              help='Benchmark ID(s)')
@click.option('-n', '--name', 'names', type=str, multiple=True,
              help='Benchmark name(s)')
@click.option('-s', '--stat', type=str, multiple=False, default='mean',
              help='Measured time stat name(s)')
@click.option('--group-id/--no-group-id', default=False,
              help='Grouping all given IDs for each name on the same plot')
def plot(ids, names, stat, group_id):
    """Plot benchmark(s) results
    """
    names = names or get_benchmark_names()
    ids = ids or [None]

    for name in names:
        ax = None

        for _id in ids:
            ax = plot_benchmark(name, stat, benchmark_id=_id, ax=ax)

            if not group_id:
                ax = None

    plt.show()
