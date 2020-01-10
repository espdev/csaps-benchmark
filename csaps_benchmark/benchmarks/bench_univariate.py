# -*- coding: utf-8 -*-

import pytest

from csaps import csaps


@pytest.mark.benchmark(
    group='univariate.make_spline',
)
def bench_make_spline(benchmark, univariate_data, size, smooth):
    x, y = univariate_data(size=size)
    benchmark(csaps, x, y, smooth=smooth)
