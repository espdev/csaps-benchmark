# -*- coding: utf-8 -*-

from typing import List, TYPE_CHECKING

import pytest
import numpy as np

if TYPE_CHECKING:
    from _pytest.python import Metafunc

from csaps_benchmark.config import config as benchmark_config


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


def pytest_generate_tests(metafunc: 'Metafunc'):
    module_name = metafunc.module.__name__.split('.')[-1].replace('bench_', '')
    func_name = metafunc.function.__name__.replace('bench_', '')

    if module_name not in benchmark_config:
        return

    module_config = benchmark_config[module_name]
    if func_name not in module_config:
        return

    func_params: List[dict] = module_config[func_name].get('parameters', {})

    for params in func_params:
        if not params:
            continue

        param_items = list(params.items())

        if len(params) == 1:
            names, values = param_items[0]
            ids = [f'{names}={v}' for v in values]
        else:
            name_list = [p[0] for p in param_items]
            value_list = [p[1] for p in param_items]

            names = ','.join(name_list)
            values = list(zip(*value_list))

            ids = []
            for vals in values:
                ids_ = []
                for name, value in zip(name_list, vals):
                    ids_.append(f'{name}={value}')
                ids.append('|'.join(ids_))

        metafunc.parametrize(names, values, ids=ids)
