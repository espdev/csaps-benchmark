# -*- coding: utf-8 -*-

import pytest

from csaps import csaps


@pytest.mark.benchmark(group='univariate.make_spline')
def bench_make_spline(benchmark, univariate_data, size, smooth):
    x, y = univariate_data(size=size)
    benchmark(csaps, x, y, smooth=smooth)


@pytest.mark.benchmark(group='univariate.evaluate_spline')
def bench_evaluate_spline(benchmark, univariate_data, output_data_sites, input_size, output_size):
    x, y = univariate_data(size=input_size)
    xi = output_data_sites(x, size=output_size)
    spline = csaps(x, y)

    benchmark(spline, xi)
