# -*- coding: utf-8 -*-

import pytest
import numpy as np


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
