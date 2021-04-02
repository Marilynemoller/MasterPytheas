#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 14:38:35 2021

@author: nathan
"""
'-------PKG---------------'
#conda install -c conda-forge windrose

from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from numpy.random import random
from numpy import arange
import pylab

#Create wind speed and direction variables
ws = random(500)*6
wd = random(500)*360

#A quick way to create new windrose axes...
def new_axes():
    fig = plt.figure(figsize=(8, 8), dpi=80, facecolor='w', edgecolor='w')
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

#...and adjust the legend box
def set_legend(ax):
    l = ax.legend(axespad=-0.10)
    plt.setp(l.get_texts(), fontsize=8)

#A stacked histogram with normed (displayed in percent) results :

ax = new_axes()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
set_legend(ax)

#Another stacked histogram representation, not normed, with bins limits

ax = new_axes()
ax.box(wd, ws, bins=arange(0,8,1))
set_legend(ax)

#A windrose in filled representation, with a controled colormap

ax = new_axes()
ax.contourf(wd, ws, bins=arange(0,8,1), cmap=cm.hot)
set_legend(ax)

#Same as above, but with contours over each filled region...

ax = new_axes()
ax.contourf(wd, ws, bins=arange(0,8,1), cmap=cm.hot)
ax.contour(wd, ws, bins=arange(0,8,1), colors='black')
set_legend(ax)