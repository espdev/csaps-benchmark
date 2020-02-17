# -*- coding: utf-8 -*-

import os
from contextlib import contextmanager
from pathlib import Path

import click
import pytest
import matplotlib.pyplot as plt
from mpl_events import MplEventConnection, MplEvent, mpl

from . import constants
from .config import load_config
from .utils import make_data_directory, get_artist_pixel_bbox
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


def dynamic_legend(event: mpl.DrawEvent):
    fig = event.canvas.figure
    axes = fig.axes[0]
    legend = axes.get_legend()

    axes_width = get_artist_pixel_bbox(axes, event.renderer).width

    legend_item_widths = []

    for line, text in zip(legend.get_lines(), legend.get_texts()):
        width = (get_artist_pixel_bbox(line, event.renderer).width +
                 get_artist_pixel_bbox(text, event.renderer).width)
        legend_item_widths.append(width)

    ncol = max(int(axes_width / max(legend_item_widths)), 1)

    axes.legend(loc='lower left', bbox_to_anchor=(0.0, 1.01), ncol=ncol,
                borderaxespad=0, frameon=False)


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

            if not hasattr(ax, 'conn'):
                ax.conn = MplEventConnection(ax, MplEvent.DRAW, dynamic_legend)

            if not group_id:
                ax = None

    plt.show()
