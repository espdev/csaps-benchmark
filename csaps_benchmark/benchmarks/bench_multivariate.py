# -*- coding: utf-8 -*-

import pytest

from csaps import csaps


@pytest.mark.benchmark(group='multivariate.make_spline')
def bench_make_spline(benchmark, multivariate_data, ndim, size):
    x, y = multivariate_data(ndim=ndim, size=size)
    benchmark(csaps, x, y)


@pytest.mark.benchmark(group='multivariate.evaluate_spline')
def bench_evaluate_spline(benchmark, multivariate_data, output_data_sites, ndim, input_size, output_size):
    x, y = multivariate_data(ndim=ndim, size=input_size)
    xi = output_data_sites(x, size=output_size)
    spline = csaps(x, y)

    benchmark(spline, xi)
