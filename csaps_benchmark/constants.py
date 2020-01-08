# -*- coding: utf-8 -*-

from pathlib import Path

DATA_PATH = Path.home() / '.csaps_benchmark'

PKG_PATH = Path(__file__).parent

PYTEST_CONFIG_PATH = PKG_PATH / 'pytest.ini'
PYTEST_CACHE_PATH = DATA_PATH / '.cache'

BENCH_PATH = PKG_PATH / 'benchmark'
BENCHMARK_STORAGE_PATH = DATA_PATH / '.benchmarks'
