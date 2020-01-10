# -*- coding: utf-8 -*-

from pathlib import Path

from pytest_benchmark.utils import get_machine_id


DATA_PATH = Path.home() / '.csaps_benchmark'

PKG_PATH = Path(__file__).parent

PYTEST_CONFIG_PATH = PKG_PATH / 'pytest.ini'
PYTEST_CACHE_PATH = DATA_PATH / '.cache'

BENCHMARKS_PATH = PKG_PATH / 'benchmarks'

BENCHMARK_STORAGE_PATH = DATA_PATH / 'benchmarks'
REPORT_STORAGE_PATH = DATA_PATH / 'reports'

BENCHMARK_MACHINE_ID_PATH = BENCHMARK_STORAGE_PATH / get_machine_id()
REPORT_MACHINE_ID_PATH = REPORT_STORAGE_PATH / get_machine_id()
