# %matplotlib inline
import pysal as ps
import pandas as pd
import numpy as np
from flask import Flask, render_template, request
from pysal.contrib.viz import mapping as maps
import matplotlib.pyplot as plt
import geopandas as gpd
import os, time, glob


def cluster():
    data = ps.pdio.read_files("C:\zoovision\data\Region1.shp")
    data.head(
        shp_link="C:\zoovision\data\Region1.shp"
    tx = gpd.read_file(shp_link)
    hr10 = ps.Quantiles(data.ind_100t, k=10)
    f, ax = plt.subplots(1, figsize=(9, 9))
    tx.assign(cl=hr10.yb).plot(column='cl', categorical=True, \
                               k=10, cmap='OrRd', linewidth=0.1, ax=ax, \
                               edgecolor='white', legend=True)
    ax.set_axis_off()
    plt.title("Incidence Deciles")
    # plt.show()

    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
    # Remove old plot files
        for
    filename in glob.glob(os.path.join('static', '*.png')):
    os.remove(filename)
    # Use time since Jan 1, 1970 in filename in order make
    # a unique filename that the browser has not chached
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    return plotfile


if __name__ == '__main__':
    print(cluster())
