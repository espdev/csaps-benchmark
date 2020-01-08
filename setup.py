# -*- coding: utf-8 -*-

import pathlib
from setuptools import setup, find_packages

ROOT_DIR = pathlib.Path(__file__).parent

NAME = 'csaps-benchmark'
PKG_NAME = NAME.translate(str.maketrans('-', '_'))


def _get_version():
    about = {}
    ver_mod = ROOT_DIR / PKG_NAME / '_version.py'
    exec(ver_mod.read_text(), about)
    return about['__version__']


def _get_long_description():
    readme = ROOT_DIR / 'README.md'
    return readme.read_text(encoding='utf-8')


setup(
    name=NAME,
    version=_get_version(),
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=[
        'pytest-benchmark',
        'click',
        'deepmerge',
        'pyyaml',
        'csaps',
    ],
    entry_points={
        'console_scripts': [
            f'{NAME} = {PKG_NAME}.cli:cli',
        ],
    },
    url='https://github.com/espdev/csaps-benchmark',
    project_urls={
        "csaps": 'https://github.com/espdev/csaps',
    },
    license='MIT',
    author='Eugene Prilepin',
    author_email='esp.home@gmail.com',
    description='An utility project for benchmarking csaps package',
    long_description=_get_long_description(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Benchmark',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
