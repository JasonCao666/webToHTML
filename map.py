from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import csv

#remove BOM
def removeBom(file):
    BOM = b'\xef\xbb\xbf'
    existBom = lambda s: True if s==BOM else False
    
    f = open(file, 'rb')
    if existBom( f.read(3) ):
        fbody = f.read()
        with open(file, 'wb') as f:
            f.write(fbody)

map = Basemap(llcrnrlon=-11.1,
              llcrnrlat=50.0,
              urcrnrlon=2.64,
              urcrnrlat=58.79,
              resolution='h', projection='lcc', width=8E6, height=8E6, lat_0 =-2.16 ,lon_0=53.87)

# draw a land-sea mask for a map background.
# lakes=True means plot inland lakes with ocean color.
map.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)
map.drawcoastlines()
map.drawcountries()

city_lons=[]
city_lats=[]
#city_names=[]
removeBom('/Users/mac/Documents/Dissertation/documents/coordination.csv')
with open('/Users/mac/Documents/Dissertation/documents/coordination.csv','rb') as csv_coordination:
    reader_coordination = csv.DictReader(csv_coordination,delimiter=',')
    for coordination in reader_coordination:
        if coordination['city']!='':
            coordination['coordination']=coordination['coordination'].replace(' ','')
            city_lons.append(float(coordination['coordination'].split(',')[1]))
            city_lats.append(float(coordination['coordination'].split(',')[0]))
    #city_names.append(str(coordination['city']))
    csv_coordination.close

print city_lons
x,y = map(city_lons, city_lats)
map.plot(x, y, 'bo', markersize=5)

'''
for label, xpt, ypt in zip(city_names, x, y):
    plt.text(xpt, ypt, label)
'''
plt.show()


