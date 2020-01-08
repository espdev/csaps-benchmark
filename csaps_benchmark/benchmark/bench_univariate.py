# -*- coding: utf-8 -*-

import pytest

from csaps import csaps


@pytest.mark.benchmark(
    group='univariate-make-spline',
)
def bench_make_spline(benchmark, univariate_data, size):
    x, y = univariate_data(size=size)
    benchmark(csaps, x, y)
