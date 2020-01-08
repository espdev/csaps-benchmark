# -*- coding: utf-8 -*-

from pathlib import Path

import click
import pytest

from .config import load_config
from .utils import make_and_return_data_path


@click.group()
@click.option('-c', '--config', 'config_path', type=Path, default=None,
              help='Benchmark configuration YAML file')
def cli(config_path):
    load_config(config_path)


@cli.command(context_settings={'ignore_unknown_options': True})
@click.argument('pytest_args', nargs=-1, type=click.UNPROCESSED)
def run(pytest_args):
    data_dir = make_and_return_data_path()

    root_dir = Path(__file__).parent
    bench_dir = root_dir / 'benchmark'
    config_path = root_dir / 'pytest.ini'
    cache_dir = data_dir / '.cache'

    benchmark_storage_dir = data_dir / '.benchmarks'

    args = [
        # pytest args
        str(bench_dir),
        '--rootdir', str(root_dir),
        '-c', str(config_path),
        '-o', f'cache_dir={cache_dir.as_posix()}',
        '-v',

        # pytest-benchmark args
        '--benchmark-only',
        '--benchmark-autosave',
        '--benchmark-storage', str(benchmark_storage_dir),
        '--benchmark-columns', 'min,max,mean,median,stddev,rounds',
        '--benchmark-sort', 'mean',

        # Additional pytest/pytest-benchmark args
        *pytest_args,
    ]

    return pytest.main(args)
