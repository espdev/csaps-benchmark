# -*- coding: utf-8 -*-

import pytest

from csaps import csaps


@pytest.mark.benchmark(
    group='univariate-make-spline',
)
@pytest.mark.parametrize('size', [
    10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000,
    25000, 50000, 75000, 100000, 250000, 500000, 750000, 1000000
])
def bench_make_spline(size, univariate_data, benchmark):
    x, y = univariate_data(size=size)
    benchmark(csaps, x, y)
