# -*- coding: utf-8 -*-

import pytest

from csaps import csaps


@pytest.mark.benchmark(group='multivariate.make_spline')
def bench_make_spline(benchmark, multivariate_data, ndim, size):
    x, y = multivariate_data(ndim=ndim, size=size)
    benchmark(csaps, x, y)
