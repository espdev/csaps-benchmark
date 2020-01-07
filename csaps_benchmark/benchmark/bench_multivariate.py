# -*- coding: utf-8 -*-

import pytest

from csaps import csaps


@pytest.mark.benchmark(
    group='multivariate-make-spline',
)
@pytest.mark.parametrize('ndim', [
    2, 3, 4, 5, 6, 7, 8, 9, 10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000
])
@pytest.mark.parametrize('size', [
    10, 50, 100, 500, 1000, 5000,
])
def bench_make_spline(ndim, size, multivariate_data, benchmark):
    x, y = multivariate_data(ndim=ndim, size=size)
    benchmark(csaps, x, y)
