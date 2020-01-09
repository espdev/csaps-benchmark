# -*- coding: utf-8 -*-

from pathlib import Path

import click
import pytest

from . import constants
from .config import load_config
from .utils import make_data_directory
from .report import make_benchmark_report_json


@click.group()
@click.option('-c', '--config', 'config_path', type=Path, default=None,
              help='Benchmark configuration YAML file')
def cli(config_path):
    load_config(config_path)


@cli.command(context_settings={'ignore_unknown_options': True})
@click.argument('pytest_args', nargs=-1, type=click.UNPROCESSED)
def run(pytest_args):
    make_data_directory()

    args = [
        # pytest args
        str(constants.BENCH_PATH),
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

    return pytest.main(args)


@cli.command()
def report():
    make_benchmark_report_json()
