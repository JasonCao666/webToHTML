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
#print distances

#read word, coordination file and save values in the list
word_coor_list=[]
with open('/Users/mac/Documents/Dissertation/documents/collection_result.csv','rb') as csv_word_coor:
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


'''#split the coordinations from string
for word_coor_row in word_coor_list:
    coordinations.append(word_coor_row['coordinations'].split())

print coordinations'''
print range(len(word_coor_list))

rigional_list=[]
wide_distributed_list=[]
#get basemap central point
for i in range(len(word_coor_list)):
    print word_coor_list[i]['word']
    distances=[]
    coor_distances=[]
    coordinations=[]
    coordinations = word_coor_list[i]['coordinations'].split()
    #print coordinations
    central_point_lon,central_point_lat=calculateCentralPoint(coordinations)
    print 'before filter central point:'+str(central_point_lon)+' '+str(central_point_lat)

    #create longi and lati list for cities and the list of coor_distances and distances
    for coor_row in coordinations:
        c_d={}
        map_p1,map_p2=map(float(coor_row.split(',')[1]),float(coor_row.split(',')[0]))
        c_d['coodination']=coor_row
        c_d['distance']=getDistanceBetweenTwoPoints(central_point_lon,central_point_lat,map_p1,map_p2)
        coor_distances.append(c_d)
        distances.append(getDistanceBetweenTwoPoints(central_point_lon,central_point_lat,map_p1,map_p2))


    #remove duplication of coordination and set filter percentage
    processDistances()
    filter_percentage=1.0
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
    
    else:
        r_distance=distances[0]
    print 'r=: '+str(r_distance)
    '''#draw the range circle on the map
    theta=np.arange(0,2*np.pi, 0.01)
    cx=(central_point_lon+r_distance*np.cos(theta))
    cy=(central_point_lat+r_distance*np.sin(theta))
    map.plot(cx,cy, color='blue', linewidth=2.0)'''

    if r_distance>=610000:
        wide_distributed_list.append(word_coor_list[i]['word'])
    else:
        rigional_list.append(word_coor_list[i]['word'])

print 'wide_distributed_list: ' + str(wide_distributed_list)
print 'rigional_list: ' + str(rigional_list)



