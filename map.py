from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

m = Basemap(width=8E6,height=8E6,projection='lcc',
            resolution=None,lat_1=48, lat_2=50, lat_0=51.51279,lon_0=-0.09184)
# draw a land-sea mask for a map background.
# lakes=True means plot inland lakes with ocean color.
m.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)
plt.show()


