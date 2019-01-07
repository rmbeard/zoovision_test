# %pip install matplotlib inline
import matplotlib.pyplot as plt
import pysal as ps
import numpy as np
import geopandas as gpd
from pysal.contrib.viz import mapping as maps
import os, time, glob

data = ps.pdio.read_files("C:\zoovision\data\Region1.shp")
fp = "C:\zoovision\data\Region1.shp"
rg1 = gpd.read_file(fp)
rg1 = rg1.to_crs(epsg=4326)
print(rg1.crs)
fig, ax = plt.subplots(1, figsize=(9, 9))
ax.set_title("Region 1")
ax.set_axis_off()
rg1.plot(ax=ax)
plt.show()

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
