import csv
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import math
from matplotlib.ticker import  MultipleLocator
from matplotlib.ticker import  FormatStrFormatter
from pylab import *

global city_shop_number
global word_coor_list
global word_distance_shop_number
global word_coordiantions
city_shop_number=[]
word_coor_list=[]
word_distance_shop_number=[]
word_coordiantions=[]

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

def getDistanceBetweenTwoPoints(lo1,la1,lo2,la2):
    distance_x=lo2-lo1
    distance_y=la2-la1
    return math.sqrt((distance_x**2)+(distance_y**2))

def calculateCentralPoint(coordinations_row):
    central_point=center_geolocation(coordinations_row)
    print central_point
    central_point_lon,central_point_lat=map(central_point[1],central_point[0])
    return central_point_lon,central_point_lat

def calculateDistanceAndShopNumber(word):
    global word_coor_list
    global word_distance_shop_number
    
    central_point_lon,central_point_lat=calculateCentralPoint(word_coordiantions)
    word_distance=[]
    for word_coor in word_coordiantions:
        map_p1,map_p2=map(float(word_coor.split(',')[1]),float(word_coor.split(',')[0]))
        distance=getDistanceBetweenTwoPoints(central_point_lon,central_point_lat,map_p1,map_p2)
        word_distance.append((word,distance))
    
    myset = set(word_distance)
    for item in myset:
        #print 'the '+str(item)+' has found'+ str(coordinations.count(item))
        shop_number=word_distance.count(item)
        word_distance_shop_number.append((item[0],item[1],shop_number))




#create basemap
map = Basemap(llcrnrlon=-11.1,
              llcrnrlat=50.0,
              urcrnrlon=2.64,
              urcrnrlat=58.79,
              resolution='l', projection='merc', lat_0 =-2.16 ,lon_0=53.87)

word_coor_list=[]
word_coordinations=[]
with open('/Users/mac/Documents/Dissertation/testDocument/carbonara.csv','rb') as csv_word_coor:
    reader_word_coors = csv.DictReader(csv_word_coor,delimiter=',')
    for word_coors in reader_word_coors:
        word_coor_dict={}
        if word_coors['word']!='':
            word_coor_dict['word']=word_coors['word']
            word_coor_dict['coordinations']=word_coors['coordinations']
            word_coordiantions=word_coors['coordinations'].split()
            word_coor_list.append(word_coor_dict)
    csv_word_coor.close

print word_coor_list
print word_coordiantions

for word_coor_row in word_coor_list:
    x=[]
    y=[]

    calculateDistanceAndShopNumber(word_coor_row['word'])
    
    word_distance_shop_number=sorted(word_distance_shop_number, key=lambda distance: distance[1])
    print word_distance_shop_number
    shop_number_sum=0
    for word_distance_shop_number_row in word_distance_shop_number:
        shop_number_sum=shop_number_sum+float(word_distance_shop_number_row[2])
        x.append(word_distance_shop_number_row[1])
        
        y.append(shop_number_sum)

    xmajorLocator = MultipleLocator(200000)
    xmajorFormatter = FormatStrFormatter('%3.1f')

    ymajorLocator = MultipleLocator(20)
    ymajorFormatter = FormatStrFormatter('%d')

    ax = subplot(111)
    plt.xlim(0,1000000)
    plt.ylim(0,250)
    plt.plot(x,y,'-ro')

    ax.xaxis.set_major_locator(xmajorLocator)
    ax.xaxis.set_major_formatter(xmajorFormatter)

    ax.yaxis.set_major_locator(ymajorLocator)
    ax.yaxis.set_major_formatter(ymajorFormatter)

    ax.xaxis.grid(True, which='major')
    ax.yaxis.grid(True, which='major')
    #plt.plot(x2,y2,label='second line')
    plt.xlabel('Distance (meter)')
    plt.ylabel('Shop Number')
    plt.title('The number of stores grows with distance')
    '''plt.legend()'''
    sum_less=0
    for distance_shop_number_row in word_distance_shop_number:
        if distance_shop_number_row[1]<= 200000:
            sum_less=sum_less+distance_shop_number_row[2]
    print 'less than 200000: '+str(sum_less)
    print 'total shop number: '+str(shop_number_sum)
    plt.show()
    





