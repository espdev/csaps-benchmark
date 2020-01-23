# -*- coding: utf-8 -*-

import pytest

from csaps import csaps


@pytest.mark.benchmark(group='ndgrid.make_spline')
def bench_make_spline(benchmark, ndgrid_data, ndim, size):
    shape = [size] * ndim
    x, y = ndgrid_data(shape=shape)
    benchmark(csaps, x, y)


@pytest.mark.benchmark(group='ndgrid.evaluate_spline')
def bench_evaluate_spline(benchmark, ndgrid_data, output_data_sites, ndim, input_size, output_size):
    shape = [input_size] * ndim
    x, y = ndgrid_data(shape=shape)
    xi = output_data_sites(x, output_size)

    spline = csaps(x, y)
    benchmark(spline, xi)
