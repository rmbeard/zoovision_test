# %matplotlib inline
import pysal as ps
import pandas as pd
import numpy as np
from flask import Flask, render_template, request
from pysal.contrib.viz import mapping as maps
import matplotlib.pyplot as plt
import geopandas as gpd
import os, time, glob


def mapper(files, title):
    fp = files
    rg1 = gpd.read_file(fp)
    rg1 = rg1.to_crs(epsg=2163)
    fig, ax = plt.subplots(1, figsize=(30, 24))
    # ax.set_title(title, y=1.08, fontsize=32)
    ax.set_axis_off()
    # minx, miny, maxx, maxy = rg1.total_bounds
    # ax.set_xlim(minx, maxx)
    # ax.set_ylim(miny, maxy)
    rg1.plot(ax=ax, column='STATE_NAME', cmap='gray')

    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old plot files
        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)
    # Use time since Jan 1, 1970 in filename in order make
    # a unique filename that the browser has not chached
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    return plotfile


if __name__ == '__main__':
    print(mapper(files, title))
