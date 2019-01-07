# -*- coding: utf-8 -*-

from climvis import plot_acinn
import numpy as np
from climvis.read_acinn import AcinnData
import random
from bokeh.plotting.figure import Figure
import os


def test_read_conv_data():

    data = plot_acinn.read_conv_data('innsbruck', 1)
    assert isinstance(data, AcinnData)


def test_speed_labels():

    spd_bins = [-1, 0, 1, 2, 3, 5, 7, 10, np.inf]
    labels = plot_acinn.speed_labels(spd_bins, 'm/s')
    assert isinstance(labels, list)
    assert 'calm' in labels


def test_plot_windrose():

    dd = random.sample(range(0, 360), 10)
    ff = random.sample(range(0, 25), 10)
    p = plot_acinn.plot_windrose(dd, ff, showp=None)
    assert isinstance(p, Figure)


def test_plot_meteo():

    data = plot_acinn.read_conv_data('innsbruck', 1)
    p1, p2 = plot_acinn.plot_meteo(data, showp=None)
    assert isinstance(p1, Figure)
    assert isinstance(p2, Figure)


def test_plot_both():

    outpath = plot_acinn.plot_both('innsbruck', 1)
    assert os.path.exists(outpath)
