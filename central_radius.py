import math
#from math import cos, sin, atan2, sqrt, pi ,radians, degrees, asin, sqrt, fabs
import csv
from mpl_toolkits.basemap import Basemap
import numpy as np
from matplotlib.patches import Ellipse, Circle
import matplotlib.pyplot as plt
import csv
from osgeo import ogr, osr

print radians(3)
#calculate the central point (specified in decimal degrees)
def center_geolocation(geolocations):
    
    x = 0
    y = 0
    z = 0
    lenth = len(geolocations)
    for row in geolocations:
        lon = radians(float(row.split(',')[0]))
        lat = radians(float(row.split(',')[1]))
        
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)
    
    x = float(x / lenth)
    y = float(y / lenth)
    z = float(z / lenth)
    return [degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y)))]

def hav(theta):
    s = sin(theta / 2)
    return s * s

#calculate the distance between two points on the earth (specified in decimal degrees)
def haversine(lon1, lat1, lon2, lat2):
    lon1=radians(lon1)
    lat1=radians(lat1)
    lon2=radians(lon2)
    lat2=radians(lat2)
    r = 6371 # earth r (km)
    dlng = fabs(lon1 - lon2)
    dlat = fabs(lat1 - lat2)
    h = hav(dlat) + cos(lat1) * cos(lat2) * hav(dlng)
    distance = 2 * r * asin(sqrt(h))*1000
    
    return distance

#The Haversine Functions to create a circle
def createCircleAroundWithRadius(lat, lon, radiusMiles):
    ring = ogr.Geometry(ogr.wkbLinearRing)
    latArray = []
    lonArray = []

    for brng in range(0,360):
        lat2, lon2 = getLocation(lat,lon,brng,radiusMiles)
        latArray.append(lat2)
        lonArray.append(lon2)
    return lonArray,latArray

def getLocation(lat1, lon1, brng, distanceMiles):
    lat1 = lat1 * math.pi/ 180.0
    lon1 = lon1 * math.pi / 180.0
    #earth radius
    R = 6378.1
    #R = ~ 3959 MilesR = 3959
            
    distanceMiles = distanceMiles/R
    brng = (brng / 90)* math.pi / 2
    lat2 = math.asin(math.sin(lat1) * math.cos(distanceMiles)+ math.cos(lat1) * math.sin(distanceMiles) * math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(distanceMiles)* math.cos(lat1),math.cos(distanceMiles)-math.sin(lat1)*math.sin(lat2))
    lon2 = 180.0 * lon2/ math.pi
    lat2 = 180.0 * lat2/ math.pi
    return lat2, lon2


word_coor_list=[]
with open('/Users/mac/Documents/Dissertation/testDocument/haggies.csv','rb') as csv_word_coor:
    reader_word_coors = csv.DictReader(csv_word_coor,delimiter=',')
    for word_coors in reader_word_coors:
        word_coor_dict={}
        if word_coors['word']!='':
            word_coor_dict['word']=word_coors['word']
            word_coor_dict['coordinations']=word_coors['coordinations']
            word_coor_list.append(word_coor_dict)
    csv_word_coor.close


map = Basemap(llcrnrlon=-11.1,
              llcrnrlat=50.0,
              urcrnrlon=2.64,
              urcrnrlat=58.79,
              resolution='h', projection='lcc', width=8E6, height=8E6, lat_0 =-2.16 ,lon_0=53.87)

map.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)
map.drawcoastlines()
map.drawcountries()

city_lons=[]
city_lats=[]
#city_names=[]
coordinations=[]
for word_coor_row in word_coor_list:
    coordinations = word_coor_row['coordinations'].split()
    central_point=center_geolocation(coordinations)
print central_point

for coor_row in coordinations:
    city_lons.append(float(coor_row.split(',')[1]))
    city_lats.append(float(coor_row.split(',')[0]))

x,y = map(city_lons, city_lats)
central_x,central_y = map(central_point[1],central_point[0])
map.plot(x, y, 'bo', markersize=5)
map.plot(central_x, central_y, '-rx', markersize=15)

'''r=2
a,b=map(-3.19474665870404,55.60749302074808)
x2,y2 = map(-3.19474665870404,55.60749302074808+r)
circle1 = plt.Circle((a, b), y2-b, color='black',fill=False)
ax.add_patch(circle1)'''

r=200000

a,b=map(-3.19474665870404,55.60749302074808)
theta=np.arange(0,2*np.pi, 0.01)
cx=a+r*np.cos(theta)
cy=b+r*np.sin(theta)
map.plot(cx,cy, color='blue', linewidth=2.0)

#test_p1,test_p2=map(-4.22398,57.47908)
print haversine(-3.19474665870404,55.60749302074808,-4.22398,57.47908)
X,Y = createCircleAroundWithRadius(55.60749302074808,-3.19474665870404,
                                   200000)

X,Y = map(X,Y)
mp.plot(X,Y,marker=None,color=c,linewidth=2)

plt.show()



