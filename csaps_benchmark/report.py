# -*- coding: utf-8 -*-

from collections import defaultdict
from typing import Optional, List
from pathlib import Path
import json

from .constants import BENCHMARK_MACHINE_ID_PATH, REPORT_MACHINE_ID_PATH
from .config import config


BENCHMARK_PAT = '*.json'


def get_latest_benchmark(pat: str = BENCHMARK_PAT):
    benchmarks = sorted(
        filter(lambda p: p.is_file(), BENCHMARK_MACHINE_ID_PATH.glob(pat)),
        key=lambda p: p.stat().st_mtime
    )

    if not benchmarks:
        return None
    return benchmarks[-1]


def get_benchmark(id: Optional[str] = None) -> Path:
    if id:
        pat = f'{id}_*.json'
    else:
        pat = BENCHMARK_PAT

    benchmark = get_latest_benchmark(pat)

    if not benchmark:
        raise RuntimeError(f"No suitable benchmarks found in '{BENCHMARK_MACHINE_ID_PATH}'")

    return benchmark


def get_benchmark_groups() -> List[str]:
    groups = []
    for module, funcs in config.items():
        for func in funcs:
            groups.append(f'{module}.{func}')
    return groups


def collect_report_info(benchmark_info):
    report_info = {}

    for group in get_benchmark_groups():
        module, func = group.split('.')

        report_info[group] = {
            'param_group': config[module][func]['param_group'],
            'param_x': config[module][func]['param_x'],
            'x': [],
            'y': {},
        }

    for benchmark in benchmark_info['benchmarks']:
        group = benchmark['group']
        module, func = group.split('.')
        group_info = report_info[group]

        param_group = benchmark['params'][group_info['param_group']]
        param_x = benchmark['params'][group_info['param_x']]

        if group_info['x'].count(param_x) == 0:
            group_info['x'].append(param_x)

        stats = group_info['y'].setdefault(param_group, defaultdict(list))
        collected_stats = set(config[module][func]['stats'])

        for stats_name, stats_value in benchmark['stats'].items():
            if stats_name in collected_stats:
                stats[stats_name].append(stats_value)

    return report_info


def make_benchmark_report_json(benchmark_id: Optional[str] = None):
    benchmark = get_benchmark(benchmark_id)

    with benchmark.open(encoding='utf8') as fp:
        benchmark_info = json.load(fp)

    report_info = {
        'machine_info': benchmark_info['machine_info'],
        'commit_info': benchmark_info['commit_info'],
        'report': collect_report_info(benchmark_info),
    }

    REPORT_MACHINE_ID_PATH.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_MACHINE_ID_PATH / benchmark.name

    with report_path.open('w', encoding='utf8') as fp:
        json.dump(report_info, fp, indent=4)
