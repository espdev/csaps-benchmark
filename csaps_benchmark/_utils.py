# -*- coding: utf-8 -*-

from pathlib import Path


def get_data_path() -> Path:
    return Path.home() / '.csaps_benchmark'
