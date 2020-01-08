# -*- coding: utf-8 -*-

from pathlib import Path

import deepmerge
import yaml

from .utils import get_root_path, get_data_path


CONFIG_FILE_NAME = 'benchmark.yml'

config = {}


def benchmark_config_paths(custom_config_path: Path = None, file_name: str = CONFIG_FILE_NAME):
    return [
        get_root_path() / file_name,
        get_data_path() / file_name,
        custom_config_path,
    ]


def config_merger():
    return deepmerge.Merger(
        type_strategies=[(dict, ["merge"]), (list, ["override"])],
        fallback_strategies=['override'],
        type_conflict_strategies=['override']
    )


def load_config(custom_config_path: Path = None):
    global config
    merger = config_merger()

    for path in benchmark_config_paths(custom_config_path):
        if path and path.exists():
            with path.open() as fp:
                merger.merge(config, yaml.safe_load(fp))

    return config
