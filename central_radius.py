import math
#from math import cos, sin, atan2, sqrt, pi ,radians, degrees, asin, sqrt, fabs
import csv
from mpl_toolkits.basemap import Basemap
import numpy as np
from matplotlib.patches import Ellipse, Circle
import matplotlib.pyplot as plt
import csv
from osgeo import ogr, osr

global coor_distances
global coordinations
global distances
coor_distances=[]
coordinations=[]
distances=[]

#calculate the central point (specified in decimal degrees)
def center_geolocation(geolocations):
    x = 0
    y = 0
    z = 0
    lenth = len(geolocations)
    for row in geolocations:
        lon = math.radians(float(row.split(',')[0]))
        lat = math.radians(float(row.split(',')[1]))
        x += math.cos(lat) * math.cos(lon)
        y += math.cos(lat) * math.sin(lon)
        z += math.sin(lat)
    
    x = float(x / lenth)
    y = float(y / lenth)
    z = float(z / lenth)
    return [math.degrees(math.atan2(y, x)), math.degrees(math.atan2(z, math.sqrt(x * x + y * y)))]

'''def hav(theta):
    s = math.sin(theta / 2)
    return s * s

#calculate the distance between two points on the earth (specified in decimal degrees)
def haversine(lon1, lat1, lon2, lat2):
    lon1=math.radians(lon1)
    lat1=math.radians(lat1)
    lon2=math.radians(lon2)
    lat2=math.radians(lat2)
    r = 6378.1 # earth r (km)
    dlng = math.fabs(lon1 - lon2)
    dlat = math.fabs(lat1 - lat2)
    h = hav(dlat) + math.cos(lat1) * math.cos(lat2) * hav(dlng)
    distance = 2 * r * math.asin(math.sqrt(h))*1000
    return distance'''

#The Haversine Functions to create a circle
def createCircleAroundWithRadius(latitude, longitude, radiusMiles):
    ring = ogr.Geometry(ogr.wkbLinearRing)
    latArray = []
    lonArray = []

    for brng in range(0,360):
        latitude2, longitude2 = getLocation(latitude,longitude,brng,radiusMiles)
        latArray.append(latitude2)
        lonArray.append(longitude2)
    return lonArray,latArray

def getLocation(latitude1, longitude1, brng, distanceMiles):
    latitude1 = latitude1 * math.pi/ 180.0
    longitude1 = longitude1 * math.pi / 180.0
    #earth radius
    R = 3959
    #R = ~ 3959 MilesR = 3959
            
    distanceMiles = distanceMiles/R
    brng = (brng / 90)* math.pi / 2
    latitude2 = math.asin(math.sin(latitude1) * math.cos(distanceMiles)+ math.cos(latitude1) * math.sin(distanceMiles) * math.cos(brng))
    longitude2 = longitude1 + math.atan2(math.sin(brng)*math.sin(distanceMiles)* math.cos(latitude1),math.cos(distanceMiles)-math.sin(latitude1)*math.sin(latitude2))
    longitude2 = 180.0 * longitude2/ math.pi
    latitude2 = 180.0 * latitude2/ math.pi
    return latitude2, longitude2

#get two points' distance in basemap
def getDistanceBetweenTwoPoints(lo1,la1,lo2,la2):
    distance_x=lo2-lo1
    distance_y=la2-la1
    return math.sqrt((distance_x**2)+(distance_y**2))

#Remove duplicate elements from the list
def removeDuplication(one_list):
    return list(set(one_list))

#After filter some coordination, update the coordination list
def updateCoordination():
    global coordinations
    global distance
    global coor_distances
    coordinations=[]
    for i in range(len(coor_distances)):
        if coor_distances[i]['distance'] in distances:
            coordinations.append(coor_distances[i]['coodination'])
        else:
            continue

#calculate basemap central point's longitude and latitude
def calculateCentralPoint(coordinations_row):
    central_point=center_geolocation(coordinations_row)
    print central_point
    central_point_lon,central_point_lat=map(central_point[1],central_point[0])
    return central_point_lon,central_point_lat

#update distances after filter
def updateDistances(central_point_lon,central_point_lat):
    global coordinations
    global distances
    distances=[]
    for coor_row in coordinations:
        map_p1,map_p2=map(float(coor_row.split(',')[1]),float(coor_row.split(',')[0]))
        distances.append(getDistanceBetweenTwoPoints(central_point_lon,central_point_lat,map_p1,map_p2))
#remove duplicate and sort distance
def processDistances():
    global distances
    distances = removeDuplication(distances)
    distances = sorted(distances,reverse = True)
    print distances

#read word, coordination file and save values in the list
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

#create basemap
map = Basemap(llcrnrlon=-11.1,
              llcrnrlat=50.0,
              urcrnrlon=2.64,
              urcrnrlat=58.79,
              resolution='l', projection='merc', lat_0 =-2.16 ,lon_0=53.87)

map.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)
map.drawcoastlines()
map.drawcountries()

#split the coordinations from string
for word_coor_row in word_coor_list:
    coordinations.append(word_coor_row['coordinations'].split())

print coordinations

#get basemap central point
central_point_lon,central_point_lat=calculateCentralPoint(coordinations[0])
print 'before filter central point:'+str(central_point_lon)+' '+str(central_point_lat)

#create longi and lati list for cities and the list of coor_distances and distances
city_lons=[]
city_lats=[]
for coor_row in coordinations:
    for word_row in coor_row:
        c_d={}
        city_lons.append(float(word_row.split(',')[1]))
        city_lats.append(float(word_row.split(',')[0]))
        map_p1,map_p2=map(float(word_row.split(',')[1]),float(word_row.split(',')[0]))
        c_d['coodination']=word_row
        c_d['distance']=getDistanceBetweenTwoPoints(central_point_lon,central_point_lat,map_p1,map_p2)
        coor_distances.append(c_d)
        distances.append(getDistanceBetweenTwoPoints(central_point_lon,central_point_lat,map_p1,map_p2))

#plot cities on the map
x,y = map(city_lons, city_lats)
map.plot(x, y, 'bo', markersize=5)

#remove duplication of coordination and set filter percentage
processDistances()
filter_percentage=0.9
filter_number=math.ceil(len(distances) * (1-filter_percentage))

#filter some cities which are far from the central point
print('after filter')
if filter_number!=0:
    print int(filter_number)
    del distances[0:int(filter_number)]
    print distances
    updateCoordination()
    central_point_lon,central_point_lat=calculateCentralPoint(coordinations)
    updateDistances(central_point_lon,central_point_lat)
    processDistances()
    r_distance=distances[0]
    print r_distance
else:
    r_distance=distances[0]

#draw the central point on the map
map.plot(central_point_lon,central_point_lat, '-rx', markersize=15)


#draw the range circle on the map
theta=np.arange(0,2*np.pi, 0.01)
cx=(central_point_lon+r_distance*np.cos(theta))
cy=(central_point_lat+r_distance*np.sin(theta))
map.plot(cx,cy, color='blue', linewidth=2.0)

#test_p1,test_p2=map(-4.22398,57.47908)
#print haversine(-3.19474665870404,55.60749302074808,-4.22398,57.47908)
#X,Y = createCircleAroundWithRadius(55.60749302074808,-3.19474665870404,r/1.6/1000)
#X,Y = map(X,Y)
#map.plot(X,Y,marker=None,color='red',linewidth=4)

#print getDistanceBetweenTwoPoints(central_point_lon,central_point_lat,c,d)
#print map.ymax - map.ymin
plt.show()



