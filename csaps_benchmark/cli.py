# -*- coding: utf-8 -*-

from datetime import datetime
from pathlib import Path

import pytest

import click


@click.group()
def cli():
    pass


@cli.command(context_settings={'ignore_unknown_options': True})
@click.argument('pytest_args', nargs=-1, type=click.UNPROCESSED)
def run(pytest_args):
    app_dir = Path.home() / '.csaps_benchmark'
    app_dir.mkdir(parents=True, exist_ok=True)

    root_dir = Path(__file__).parent
    config_path = root_dir / 'pytest.ini'
    cache_dir = app_dir / '.cache'

    benchmark_storage_dir = app_dir / '.benchmarks'

    args = [
        # pytest args
        '--rootdir', str(root_dir),
        '-c', str(config_path),
        '-o', 'cache_dir={}'.format(cache_dir.as_posix()),
        '-v',

        # pytest-benchmark args
        '--benchmark-only',
        '--benchmark-autosave',
        '--benchmark-storage', str(benchmark_storage_dir),
        '--benchmark-columns', 'min,max,mean,median,stddev,rounds',
        '--benchmark-sort', 'name',

        # Additional pytest/pytest-benchmark args
        *pytest_args,
    ]

    return pytest.main(args)
