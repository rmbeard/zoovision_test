# %matplotlib inline
from lisa_test import moran_inverse, moran_gen
from matplotlib.widgets import Slider, Button, RadioButtons
import pysal as ps
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np
from pandas import DataFrame
import os, time, glob


def maps1(files, selected_risk, selected_season, selected_week):
    df = pd.read_csv('C:\zoovision\data\weeklydata.csv')
    fp = files
    rg1 = gpd.read_file(fp)

    # df = df[['SEASON'] == '2015-16']
    df1 = df['SEASON'] == selected_season
    # print(df1)
    df = df[df1]
    # print(df)

    df1 = df['WEEK'] == selected_week
    # print(df1)
    df = df[df1]

    df = df[['SEASON', 'STATE_NAME', 'WEEK', 'PERCENT POSITIVE', '%UNWEIGHTED ILI']]
    # print(df)
    #rg1 = rg1.to_crs(epsg=2163)
    rg1 = rg1.merge(df, on='STATE_NAME')
    # print(rg1)
    # print(rg1.dtypes)
    fig, ax = plt.subplots(1, figsize=(14, 8))
    title = selected_season + " " + selected_risk + " " + 'WEEK' + " " + str(selected_week)
    ax.set_title(title, y=1.08, fontsize=20)
    ax.set_axis_off()
    rg1.plot(column=selected_risk, categorical=True, k=10, cmap='OrRd', linewidth=0.3, ax=ax,
                           edgecolor='black', legend=False)
    vmin, vmax = 0, 0
    for i in df[selected_risk]:
        if i >= vmax:
            vmax = i
    sm = plt.cm.ScalarMappable(cmap='OrRd', norm = plt.Normalize(vmin=vmin, vmax=vmax))
    # empty array for the data range
    sm._A = []
    # add the colorbar to the figure
    cbar = fig.colorbar(sm)
    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old plot files
        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)
    # Use time of filename in order make a unique filename that the browser has not chached
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    plt.close()
    plotfile1 = plotfile
    # plt.show()
    return plotfile1


def mapper(files):
    fp = files
    rg1 = gpd.read_file(fp)
    rg1 = rg1.to_crs(epsg=2163)
    fig, ax = plt.subplots(1, figsize=(15, 10))
    selected = "POP10_SQMI"
    if selected == "POP10_SQMI":
        hr10 = ps.Quantiles(rg1.POP10_SQMI, k=10)
    else:
        hr10 = ps.Quantiles(rg1.POP10_SQMI, k=10)
    title = "Select parameters and press query to view surveillance summary"
    ax.set_title(title, y=1.08, fontsize=30)
    ax.set_axis_off()
    # minx, miny, maxx, maxy = rg1.total_bounds
    # ax.set_xlim(minx, maxx)
    # ax.set_ylim(miny, maxy)
    rg1.plot(ax=ax)
    # rg1.assign(cl=hr10.yb).plot(column='cl', categorical=True, \
    #                  linewidth=0.5, ax=ax,
    #                  k = 10, cmap='BuGn', edgecolor='black')

    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old plot files
        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)
    # Use time in filename in order make a unique filename that the browser has not chached
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    # print(rg1.dtypes)
    return plotfile


def mapper_test(files, db_result, selected_virus, selected_risk, risk_factor):
    fp = files
    rg1 = gpd.read_file(fp)
    df = DataFrame(db_result.fetchall())
    df.columns = db_result.keys()
    df.columns = df.columns.str.upper()
    # print(df)
    # print(rg1)
    # print(tuple(df))
    # print(tuple(rg1))
    rg1 = rg1.to_crs(epsg=2163)
    # df.STATE_NAME.astype(str)
    # rg1.STATE_NAME.astype(str)
    # print(df.dtypes)
    # print(rg1.dtypes)
    rg1 = rg1.merge(df, on='STATE_NAME')
    # print(rg1.dtypes)
    fig, ax = plt.subplots(1, figsize=(15, 10))

    title = 'National ' + selected_risk
    ax.set_title(title, y=1.08, fontsize=30)
    ax.set_axis_off()
    if selected_virus == "FLU_PDM":
        rg1.plot(column=selected_risk, categorical=True, k=10, cmap='OrRd', linewidth=0.3, ax=ax,
                           edgecolor='black', legend=False)
    # if selected_risk == "Prevalence"
    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old plot files
        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)
    # Use time of filename in order make a unique filename that the browser has not chached
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    plt.close()
    return plotfile


def local_moran(files, weight):
    fp = files
    rg1 = gpd.read_file(fp)
    rg1 = rg1.to_crs(epsg=2163)
    # fig, ax = plt.subplots(1, figsize=(12, 12))
    # ax.set_title("Local Indicators of Spatial Association ", y=1.08, fontsize=42)
    # ax.set_axis_off()
    # retrieve cluster classifications
    if weight == 'Inverse Distance':
        moran_inverse(rg1)
    else:
        moran_gen(rg1)
        # need to fix
    # hmap = colors.ListedColormap(['white', 'red', 'lightblue', 'blue', 'pink'])
    # # f, ax = plt.subplots(1, figsize=(9, 9))
    # rg1.assign(cl=labels).plot(column='cl', categorical=True, k=5, cmap=hmap, linewidth=0.5, ax=ax,
    #                             edgecolor='black', legend=True)
    # ax.set_axis_off()
    # plt.show()
    # plt.legend(loc='lower left', fancybox=True)
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


fig, ax = plt.subplots(1, figsize=(15, 10))


def slider():
    fp = "C:\zoovision\data\states\states2.shp"
    rg1 = gpd.read_file(fp)
    rg1 = rg1.to_crs(epsg=2163)
    # fig, ax = plt.subplots(1, figsize=(15, 10))
    hr10 = ps.Quantiles(rg1.POP10_SQMI, k=10)
    # title = "Select parameters and press query to view surveillance summary"
    # ax.set_title(title, y=1.08, fontsize=30)
    ax.set_axis_off()
    rg1.plot(ax=ax)

    # define demnsions of slider bar
    axcolor = 'lightgoldenrodyellow'
    axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

    # mapslider= plt.axes
    samp = Slider(axfreq, 'Week', 1, 40, valinit=1)
    samp.on_changed(update)
    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old plot files
        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)
    # Use time in filename in order make a unique filename that the browser has not chached
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    plt.show()
    return plotfile


def sum_chart():
    n = 3
    H1N1 = (16, 21, 23)
    H3N2 = (21, 11, 21)
    x = np.arange(n)
    width = 0.35
    fig, ax = plt.subplots(1, figsize=(6, 4))
    p1 = plt.bar(x, H3N2, width, color='black')
    p2 = plt.bar(x, H1N1, width, color='firebrick', bottom=H3N2)
    plt.ylabel('Percent')
    plt.title('Proportion of Circulating viral sequences by species')
    plt.xticks(x, ('Human', 'Avian', 'Swine'))
    plt.yticks(np.arange(0, 60, 5))
    plt.legend((p2[0], p1[0]), ('H1N1', 'H3N2'))
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    plt.close()
    return plotfile


def update(val):
    fig.canvas.draw_idle()


if __name__ == '__main__':
    print(mapper(files, title))
    print(mapper2(files, title))
