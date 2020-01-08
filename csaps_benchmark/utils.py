# -*- coding: utf-8 -*-

from .constants import DATA_PATH


def make_data_directory():
    DATA_PATH.mkdir(parents=True, exist_ok=True)
