import math
#from math import cos, sin, atan2, sqrt, pi ,radians, degrees, asin, sqrt, fabs
import csv
from mpl_toolkits.basemap import Basemap
import numpy as np
from matplotlib.patches import Ellipse, Circle
import matplotlib.pyplot as plt
import csv
from osgeo import ogr, osr
import os

global coor_distances
global coordinations
global previous_coordinations
global distances
global city_shop_number
global original_central_lon
global original_central_lat
coor_distances=[]
coordinations=[]
distances=[]
city_shop_number=[]
previous_coordinations=[]

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
    global coor_distances
    coordinations=[]
    for coor_dis_row in coor_distances:
        coordinations.append(coor_dis_row['coodination'])

#calculate basemap central point's longitude and latitude
def calculateCentralPoint(coordinations_row):
    global original_central_lon
    global original_central_lat
    
    central_point=center_geolocation(coordinations_row)
   
    original_central_lon=float(central_point[1])
    original_central_lat=float(central_point[0])
    #print str(original_central_lon)+str(original_central_lat)
    central_point_lon,central_point_lat=map(central_point[1],central_point[0])
    return central_point_lon,central_point_lat

#update distances after filter
def updateDistances(central_point_lon,central_point_lat):
    global previous_coordinations
    global distances
    print str(len(coordinations))+' '+str(len(previous_coordinations))
    distances=[]
    for coor_row in previous_coordinations:
        map_p1,map_p2=map(float(coor_row.split(',')[1]),float(coor_row.split(',')[0]))
        distances.append(getDistanceBetweenTwoPoints(central_point_lon,central_point_lat,map_p1,map_p2))

#get redius
def getRadius(central_point_lon,central_point_lat):
    global coordinations
    r_distances_sort=[]
    for coors in coordinations:
        map_p1,map_p2=map(float(coors.split(',')[1]),float(coors.split(',')[0]))
        r_distances_sort.append(getDistanceBetweenTwoPoints(central_point_lon,central_point_lat,map_p1,map_p2))
    
    r_distances_sort = removeDuplication(r_distances_sort)
    r_distances_sort = sorted(r_distances_sort,reverse = True)
    return r_distances_sort[0]

#remove duplicate and sort distance
def processDistances():
    global distances
    distances = removeDuplication(distances)
    distances = sorted(distances,reverse = True)

def calculateShopNumber():
    global city_shop_number
    city_shop_number=[]
    myset = set(previous_coordinations)
    for item in myset:
        city_shop_number_dic={}
        #print 'the '+str(item)+' has found'+ str(coordinations.count(item))
        city_shop_number_dic[item]=previous_coordinations.count(item)
        city_shop_number.append(city_shop_number_dic)

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

output_list=[]
#get basemap central point
for i in range(len(word_coor_list)):
    #print word_coor_list[i]['word']
    distances=[]
    coor_distances=[]
    coordinations=[]
    coordinations = word_coor_list[i]['coordinations'].split()
    previous_coordinations = word_coor_list[i]['coordinations'].split()
    #print coordinations
    central_point_lon,central_point_lat=calculateCentralPoint(coordinations)
    #print 'before filter central point:'+str(central_point_lon)+' '+str(central_point_lat)
    
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
    filter_percentage=0.95
    filter_number=math.ceil(len(coor_distances) * (1-filter_percentage))
    
    #filter some cities which are far from the central point

    if filter_number!=0 and len(coor_distances)!=1:
        coor_distances = sorted(coor_distances, key=lambda coor_distances: coor_distances['distance'], reverse = True)
        del coor_distances[0:int(filter_number)]
        updateCoordination()
        
        central_point_lon,central_point_lat=calculateCentralPoint(coordinations)
        updateDistances(central_point_lon,central_point_lat)
        processDistances()
    
    calculateShopNumber()
    for city_n in city_shop_number:
        for key,value in city_n.items():
            word_score_shops=[]
            word_score_shops.append(word_coor_list[i]['word'])
            cor1,cor2=map(float(key.split(',')[1]),float(key.split(',')[0]))
            word_score_shops.append(round(getDistanceBetweenTwoPoints(central_point_lon,central_point_lat,cor1,cor2),2))
            word_score_shops.append(value)
            word_score_shops.append(original_central_lon)
            word_score_shops.append(original_central_lat)
            word_score_shops.append(getRadius(central_point_lon,central_point_lat))
            output_list.append(word_score_shops)



#if file exist, delete
output_filename = '/Users/mac/Documents/Dissertation/documents/word_score_shop.csv'
if os.path.exists(output_filename):
    os.remove(output_filename)

#write result into wordLocation.csv
headers = ['word', 'distance_centre', 'shop_number', 'word_central_lon', 'word_central_lat','radius']
with open(output_filename,'wb') as output_file:
    csvWriter = csv.writer(output_file)
    csvWriter.writerow(headers)
    for data in output_list:
        csvWriter.writerow(data)
output_file.close

   






