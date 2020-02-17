# -*- coding: utf-8 -*-

from .constants import DATA_PATH
from typing import NamedTuple


def make_data_directory():
    DATA_PATH.mkdir(parents=True, exist_ok=True)


class BBox(NamedTuple):
    x0: int
    x1: int
    y0: int
    y1: int
    width: int
    height: int


def get_artist_pixel_bbox(artist, renderer=None):
    fig = artist.figure

    if fig is None:
        fig = artist

    bbox = artist.get_window_extent(renderer=renderer).transformed(fig.dpi_scale_trans.inverted())
    x0, x1, y0, y1, width, height = bbox.x0, bbox.x1, bbox.y0, bbox.y1, bbox.width, bbox.height

    x0 *= fig.dpi
    x1 *= fig.dpi
    y0 *= fig.dpi
    y1 *= fig.dpi
    width *= fig.dpi
    height *= fig.dpi

    return BBox(x0, x1, y0, y1, width, height)
