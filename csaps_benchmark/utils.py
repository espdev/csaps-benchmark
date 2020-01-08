# -*- coding: utf-8 -*-

from pathlib import Path


def get_root_path() -> Path:
    return Path(__file__).parent


def get_data_path() -> Path:
    return Path.home() / '.csaps_benchmark'


def make_and_return_data_path() -> Path:
    path = get_data_path()
    path.mkdir(parents=True, exist_ok=True)
    return path
