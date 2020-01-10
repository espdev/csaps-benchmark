# -*- coding: utf-8 -*-

from collections import defaultdict
from typing import Optional, List
from pathlib import Path
import json

import matplotlib.pyplot as plt

from .constants import BENCHMARK_MACHINE_ID_PATH, REPORT_MACHINE_ID_PATH
from .config import config


BENCHMARK_PAT = '*.json'


def get_latest_benchmark(pat: str = BENCHMARK_PAT):
    benchmarks = sorted(
        filter(lambda p: p.is_file(), BENCHMARK_MACHINE_ID_PATH.glob(pat)),
        key=lambda p: p.stat().st_mtime
    )

    if not benchmarks:
        raise RuntimeError(
            f"No benchmarks found for the pattern '{pat}' in '{BENCHMARK_MACHINE_ID_PATH}'")

    return benchmarks[-1]


def get_benchmark(id: Optional[str] = None) -> Path:
    if id:
        pat = f'{id}_*.json'
    else:
        pat = BENCHMARK_PAT

    return get_latest_benchmark(pat)


def get_benchmark_names() -> List[str]:
    names = []
    for module, funcs in config['benchmarks'].items():
        for func in funcs:
            names.append(f'{module}.{func}')
    return names


def collect_report_info(benchmark_info):
    report_info = {}
    benchmarks_config = config['benchmarks']

    for name in get_benchmark_names():
        module, func = name.split('.')

        report_info[name] = {
            'param_group': benchmarks_config[module][func]['param_group'],
            'param_x': benchmarks_config[module][func]['param_x'],
            'x': [],
            'y': {},
        }

    collected_stats = config['report']['stats']

    for benchmark in benchmark_info['benchmarks']:
        name = benchmark['group']
        module, func = name.split('.')
        info_by_name = report_info[name]

        param_group = benchmark['params'][info_by_name['param_group']]
        param_x = benchmark['params'][info_by_name['param_x']]

        if info_by_name['x'].count(param_x) == 0:
            info_by_name['x'].append(param_x)

        stats = info_by_name['y'].setdefault(param_group, defaultdict(list))

        for stats_name, stats_value in benchmark['stats'].items():
            if stats_name in collected_stats:
                stats[stats_name].append(stats_value)

    return report_info


def load_json_data(json_path: Path) -> dict:
    with json_path.open(encoding='utf8') as fp:
        return json.load(fp)


def make_benchmark_report_json(benchmark_id: Optional[str] = None):
    benchmark_path = get_benchmark(benchmark_id)
    benchmark_info = load_json_data(benchmark_path)

    report_info = {
        'machine_info': benchmark_info['machine_info'],
        'commit_info': benchmark_info['commit_info'],
        'report': collect_report_info(benchmark_info),
    }

    REPORT_MACHINE_ID_PATH.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_MACHINE_ID_PATH / benchmark_path.name

    with report_path.open('w', encoding='utf8') as fp:
        json.dump(report_info, fp, indent=4)


def plot_benchmark(benchmark_name: str, statistic: str = 'mean',
                   benchmark_id: Optional[str] = None):
    benchmark_path = get_benchmark(benchmark_id)
    benchmark_id = str(benchmark_path.name).split('_')[0]

    report_path = REPORT_MACHINE_ID_PATH / benchmark_path.name

    if not report_path.exists():
        make_benchmark_report_json(benchmark_id)

    report_info = load_json_data(report_path)

    benchmark_report = report_info['report'][benchmark_name]

    param_group = benchmark_report['param_group']
    param_x = benchmark_report['param_x']
    x_data = benchmark_report['x']
    y = benchmark_report['y']

    fig, ax = plt.subplots(1, 1)

    legend = []
    for param_value, stats in y.items():
        y_data = stats[statistic]
        ax.loglog(x_data, y_data, '.-')
        legend.append(f'{param_group}={param_value}')

    ax.set_title(f'{benchmark_name} (ID: {benchmark_id})')
    ax.set_xlabel(param_x)
    ax.set_ylabel('time, [seconds]')
    ax.grid(True)
    ax.legend(legend)

    return fig, ax
