from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

map = Basemap(llcrnrlon=-11.1,
              llcrnrlat=50.0,
              urcrnrlon=2.64,
              urcrnrlat=58.79,
              resolution='h', projection='lcc', width=8E6, height=8E6, lat_0 =-2.16 ,lon_0=53.87)
# draw a land-sea mask for a map background.
# lakes=True means plot inland lakes with ocean color.
map.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)
map.drawcoastlines()
plt.show()


