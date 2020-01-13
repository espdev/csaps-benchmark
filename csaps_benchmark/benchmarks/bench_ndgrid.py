# -*- coding: utf-8 -*-

import pytest

from csaps import csaps


@pytest.mark.benchmark(group='ndgrid.make_spline')
def bench_make_spline(benchmark, ndgrid_data, ndim, size):
    shape = [size] * ndim
    x, y = ndgrid_data(shape=shape)
    benchmark(csaps, x, y)
