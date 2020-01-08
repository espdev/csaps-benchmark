# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List

import pytest
from _pytest.python import Metafunc
import toml
from deepmerge import Merger
import numpy as np

from csaps_benchmark import get_data_path


def pytest_addoption(parser):
    parser.addoption('--benchmark-params-toml', type=Path, default=None,
                     help='Benchmark parameters config TOML file.')


def root_path() -> Path:
    return Path(__file__).parent.parent


def data_path() -> Path:
    path = get_data_path()
    path.mkdir(parents=True, exist_ok=True)
    return path


def benchmark_toml_paths(config):
    file_name = 'benchmark.toml'

    return [
        root_path() / file_name,
        data_path() / file_name,
        config.getoption('--benchmark-params-toml'),
    ]


def params_merger():
    return Merger(
        type_strategies=[(dict, ["merge"]), (list, ["override"])],
        fallback_strategies=['override'],
        type_conflict_strategies=['override']
    )


def benchmark_params(config):
    merger = params_merger()
    params = {}

    for path in benchmark_toml_paths(config):
        if path and path.exists():
            with path.open() as fp:
                merger.merge(params, toml.load(fp))

    return params


@pytest.fixture(scope='session')
def univariate_data():
    def data(size, seed=1234):
        np.random.seed(seed)
        x = np.linspace(-10., 10., size)
        y = np.exp(-(x / 2.5) ** 2) + (np.random.rand(size) - 0.2) * 0.3
        return x, y

    return data


@pytest.fixture(scope='session')
def multivariate_data():
    def data(ndim, size, seed=1234):
        np.random.seed(seed)
        x = np.linspace(0, np.pi * 2, size)
        y = np.sin(x) + np.random.randn(ndim, size) * 0.15
        return x, y

    return data


def pytest_generate_tests(metafunc: Metafunc):
    module_name = metafunc.module.__name__.split('.')[-1].replace('bench_', '')
    func_name = metafunc.function.__name__.replace('bench_', '')

    params_config = benchmark_params(metafunc.config)
    if module_name not in params_config:
        return

    module_context = params_config[module_name]
    if func_name not in module_context:
        return

    param_list: List[dict] = module_context[func_name]

    for params in param_list:
        if not params:
            continue

        param_items = list(params.items())

        if len(params) == 1:
            names, values = param_items[0]
            ids = [f'{names}={v}' for v in values]
        else:
            names_list = [p[0] for p in param_items]
            values_list = [p[1] for p in param_items]

            names = ','.join(names_list)
            values = list(zip(*values_list))

            ids = []
            for vals in values:
                ids_ = []
                for name, value in zip(names_list, vals):
                    ids_.append(f'{name}={value}')
                ids.append('|'.join(ids_))

        metafunc.parametrize(names, values, ids=ids)
