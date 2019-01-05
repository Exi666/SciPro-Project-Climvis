# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 16:10:03 2018

@author: Birgit Bacher
"""

from bokeh.plotting import figure, show, output_file
from bokeh import palettes
from bokeh.models import Range1d, DatetimeTickFormatter
from bokeh.layouts import gridplot
from math import radians
import numpy as np
import pandas as pd


def speed_labels(bins, units):
    """
    Generates labels for windspeed bins

    Input
    ----------
    bins: Windspeed bins
    units: = Unit
    """
    labels = []
    for left, right in zip(bins[:-1], bins[1:]):
        if left == bins[0]:
            labels.append('calm'.format(right))
        elif np.isinf(right):
            labels.append('>{} {}'.format(left, units))
        else:
            labels.append('{} - {} {}'.format(left, right, units))

    return list(labels)


def plot_windrose(dd, ff, wndspd_units='m/s', spd_bins=None):
    """
    Plots Windrose with bokeh

    Input
    ----------
    dd:         Winddirection
    ff:         Windspeed

    Parameters:
    ----------
    wndspd_units = 'm/s'
    spd_bins = None         Categories for windspeed - should end with np.inf

    """

    # -------------------------------------------------------------------------
    #  preparing data
    # -------------------------------------------------------------------------
    if spd_bins is None:
        spd_bins = [-1, 0, 1, 2, 3, 5, 7, 10, np.inf]  # get speed bins

    # get categorizations for speed & direction
    spd_labels = speed_labels(spd_bins, wndspd_units)  # get speed labels
    dir_bins = np.arange(-7.5, 370, 15)  # get wind directory categories
    dir_labelsf = (dir_bins[:-1] + dir_bins[1:]) / 2  # labels for directions
    dir_labels = dir_labelsf.astype(int)  # get rid of the commas for labels
    dir_labels = dir_labels.astype(str)  # convert into string

    # categorize data
    WindSpd_bins = pd.cut(ff, bins=spd_bins, labels=spd_labels, right=True)
    WindDir_bins = pd.cut(dd, bins=dir_bins, labels=dir_labels, right=False)
    # get frequency table
    tab = pd.crosstab(WindDir_bins, WindSpd_bins, dropna=False)

    # -------------------------------------------------------------------------
    # setting things up for plot
    # -------------------------------------------------------------------------

    width = 800
    height = 800
#    inner_radius = 0
#    outer_radius = 300 - 10
    palette = palettes.brewer['Spectral'][len(spd_bins)]  # color palette

    p = figure(plot_width=width,
               plot_height=height,
               title="Windrose",
               x_axis_type=None,
               y_axis_type=None,
               tools="pan,wheel_zoom,save,reset")

    # -------------------------------------------------------------------------
    # plot wind data
    # -------------------------------------------------------------------------

    for i in range(len(dir_bins)-1):  # last angle not needed
        # loop over each angle to get starting & ending angle for wedges
        # -90 because coordinate system starts from horizontal
        startangle = -radians(dir_bins[i+1] - 90)
        endangle = -radians(dir_bins[i] - 90)
        # reset of those two after each angle:
        spdcnt = 0  # counter for windspeed frequencies
        palcnt = 0  # counter for colorpalette

        for wndspd in tab.loc[dir_labels[i]]:
            # loop over each windspeed
            tmpcnt = spdcnt + wndspd  # temporary variables for size of slices
            p.annular_wedge(0, 0,  # starting coordinates
                            spdcnt,  # inner radius for slice
                            tmpcnt,  # outer radius for slice
                            startangle, endangle,  # angles for wedges
                            legend=WindSpd_bins.categories[palcnt],  # legend
                            fill_color=palette[palcnt],  # fill with color
                            line_color=None,
                            direction="anticlock"
                            )
            spdcnt = tmpcnt
            palcnt += 1

    # -------------------------------------------------------------------------
    # setting up "coordinate system" for "polar plot"
    # -------------------------------------------------------------------------

    # set up angles and labels for cardinal points of "coordinate system"
    ind = ['N', 'NO', 'O', 'SO', 'S', 'SW', 'W', 'NW', 'N']
    angles_deg = pd.Series(np.linspace(0, 360, 9), index=ind)
    # get size of scaling rings
    max_cls = max(tab.sum(axis=1))
    # get radii of the inner rings for "coordinate system"
    radii = np.linspace(0, max_cls, num=6)
    radii = radii.round()
    # coordinates for ring-labels
    half_angle = radians(angles_deg[1]/2)  # needed for text skewness too
    xr = radii[1:]*np.cos(np.array(radians(45) + half_angle))
    yr = radii[1:]*np.sin(np.array(radians(45) + half_angle))
    radii = radii.astype(int)
    radii = radii.astype(str)
    maxrad = int(radii[-1])

    # -------------------------------------------------------------------------
    # plotting up "coordinate system"
    # -------------------------------------------------------------------------

    # radius lines for frequency
    p.circle(0, 0, radius=radii, fill_color=None, line_color="grey")
    # text for frequency
    p.text(xr, yr, [str(r) for r in radii[1:]],
           angle=-half_angle,
           text_font_size="10pt",
           text_align="center",
           text_color="grey")

    # circular axes
    p.annular_wedge(0, 0, 0, maxrad + maxrad / 30,
                    angles_deg, angles_deg, color="grey",
                    end_angle_units="deg", start_angle_units="deg")

    # orientation text
    # doesn't work with simple "radians" - has to be np.radians - why ever...
    txr = (maxrad + maxrad / 10) * np.sin(np.radians(angles_deg))
    tyr = (maxrad + maxrad / 10) * np.cos(np.radians(angles_deg))
    p.text(txr.values[0:-1], tyr.values[0:-1], ind[0:-1],
           color="grey", text_align="center")

    # adapt plotsize
    p.x_range = Range1d((-max_cls - max_cls / 4), (max_cls + max_cls / 4))
    p.y_range = Range1d((-max_cls - max_cls / 4), (max_cls + max_cls / 4))

    output_file("windrose.html")
    show(p)


def plot_meteo(acdat):
    """
    Plot Meteorological Data from ACINN Station

    Input
    ----------
    acdat:      AcinnData-Object fom read_acinn.py
                needs those Methods to be run, before importing:
                    self.get_data()
                    self.conv_raw()
                    self.conv_date()
                    self.conv_units()
                    self.make_dict()
    """
    # plot Temperature & Dewpoint
    p1 = figure(x_axis_type="datetime", title="Temperature, Dewpoint")
    p1.grid.grid_line_alpha = 0.3
    p1.yaxis.axis_label = acdat.dict['tl']
    p1.line(acdat.timeutc, acdat.tl, color='red', legend=acdat.dict['tl'])
    p1.line(acdat.timeutc, acdat.tp, color='green', legend=acdat.dict['tp'])
    p1.xaxis.formatter = DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
            )
    p1.xaxis.major_label_orientation = np.pi/4

    # plot Precipitationrate & Precipitation
    p2 = figure(x_axis_type="datetime",
                title="Precipitationrate, Precipitation")
    p2.grid.grid_line_alpha = 0.3
    p2.yaxis.axis_label = 'Precipitation [mm]'
    p2.line(acdat.timeutc, acdat.crm, color='blue', legend=acdat.dict['crm'])
    p2.vbar(x=acdat.timeutc, top=acdat.rr, width=0.9, alpha=0.5)
    p2.xaxis.formatter = DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
            )
    p2.xaxis.major_label_orientation = np.pi/4
    p2.legend.location = "top_left"

    output_file("meteo.html")
    show(gridplot([[p1], [p2]], plot_width=800, plot_height=400))
