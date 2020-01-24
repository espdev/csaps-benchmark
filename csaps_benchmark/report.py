# -*- coding: utf-8 -*-

from collections import defaultdict
from typing import Optional, List
from pathlib import Path
import json

import pandas as pd
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


def load_json_data(json_path: Path) -> dict:
    with json_path.open(encoding='utf8') as fp:
        return json.load(fp)


def make_benchmark_report():
    latest_benchmark_path = get_benchmark()
    benchmark_info = load_json_data(latest_benchmark_path)
    reports = {}

    for benchmark in benchmark_info['benchmarks']:
        name = benchmark['group']

        report = reports.setdefault(name, {
            'name': name,
            'options': benchmark['options'],
            'extra_info': benchmark['extra_info'],
            'params': defaultdict(list),
            'stats': defaultdict(list),
        })

        for pname, pvalue in benchmark['params'].items():
            report['params'][pname].append(pvalue)

        for sname, svalue in benchmark['stats'].items():
            report['stats'][sname].append(svalue)

    report_info = {
        'machine_info': benchmark_info['machine_info'],
        'commit_info': benchmark_info['commit_info'],
        'benchmarks': reports,
    }

    REPORT_MACHINE_ID_PATH.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_MACHINE_ID_PATH / latest_benchmark_path.name

    with report_path.open('w', encoding='utf8') as fp:
        json.dump(report_info, fp, indent=4)


def get_report_dataframe(benchmark_report: dict, fillna: float = -1.0):
    data = benchmark_report['params'].copy()
    stats_names = config['report']['stats']

    for stat_name, stat_values in benchmark_report['stats'].items():
        if stat_name in stats_names:
            data[stat_name] = stat_values

    return pd.DataFrame(data).fillna(fillna)


def plot_benchmark(benchmark_name: str, stat: str = 'mean',
                   benchmark_id: Optional[str] = None):
    benchmark_path = get_benchmark(benchmark_id)
    benchmark_id = str(benchmark_path.name).split('_')[0]

    report_path = REPORT_MACHINE_ID_PATH / benchmark_path.name
    report_info = load_json_data(report_path)

    module, func = benchmark_name.split('.')
    benchmark_config = config['benchmarks'][module][func]
    benchmark_report = report_info['benchmarks'][benchmark_name]
    benchmark_df = get_report_dataframe(benchmark_report)

    groupby_params = benchmark_config['groupby']
    param_x = benchmark_config['x']

    with plt.style.context('ggplot'):
        plt.rcParams['figure.autolayout'] = True

        fig, ax = plt.subplots(1, 1)

        for group, df in benchmark_df.groupby(groupby_params):
            x_data = df[param_x]
            y_data = df[stat]

            if not isinstance(group, (list, tuple)):
                group = [group]

            gr = zip(groupby_params, group)
            label = '|'.join(f'{n}={v}' for n, v in gr)

            ax.plot(x_data, y_data, '.-', label=label)

        # ax.set_title(f'{benchmark_name} (ID: {benchmark_id})')
        ax.set_xlabel(param_x)
        ax.set_ylabel(f'{stat} time, [seconds]')
        ax.legend(loc='lower left', bbox_to_anchor=(0.0, 1.01), ncol=2,
                  borderaxespad=0, frameon=False)
        ax.grid(True)

    return fig, ax
