# %pip install matplotlib inline
import matplotlib.pyplot as plt
import pysal as ps
import numpy as np
import geopandas as gpd
from pysal.contrib.viz import mapping as maps

shp_link = ps.examples.get_path('NAT.shp')
tx = gpd.read_file(shp_link)
print('Reading from ', shp_link)

hr90 = np.array(ps.open(shp_link.replace('.shp', '.dbf')).by_col('HR90'))

w = ps.queen_from_shapefile(shp_link)
lisa = ps.Moran_Local(hr90, w, permutations=9999)

p_thres = 0.01
f, ax = plt.subplots(1, figsize=(9, 9))
# boxes, labels = maps.lisa_legend_components(lisa, p_thres=p_thres)
# plt.legend(boxes, labels, loc='lower left', fancybox=True)
tx.assign(cl=lisa).plot(column='cl', categorical=True, \
                        k=10, cmap='OrRd', linewidth=0.1, ax=ax, \
                        edgecolor='white', legend=True)
ax.set_axis_off()
plt.title('HR90 | LISA clusters | P-value = %.2f' % p_thres)

plt.show()
