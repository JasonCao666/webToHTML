import csv
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import math
from matplotlib.ticker import  MultipleLocator
from matplotlib.ticker import  FormatStrFormatter
from pylab import *
import os

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
    word_distance_shop_number=[]
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

def avgFind(lst):
    b=len(lst)
    sum=0
    for i in lst:
        sum=sum+float(i[1])
    return sum/b

#create basemap
map = Basemap(llcrnrlon=-11.1,
              llcrnrlat=50.0,
              urcrnrlon=2.64,
              urcrnrlat=58.79,
              resolution='l', projection='merc', lat_0 =-2.16 ,lon_0=53.87)

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

output_list=[]
for word_coor_row in word_coor_list:
    x=[]
    y=[]
    word_coordinations=[]
    word_coordiantions=word_coor_row['coordinations'].split()
    calculateDistanceAndShopNumber(word_coor_row['word'])
    word_distance_shop_number=sorted(word_distance_shop_number, key=lambda distance: distance[1])
    #print word_distance_shop_number
    shop_number_sum=0
    for word_distance_shop_number_row in word_distance_shop_number:
        shop_number_sum=shop_number_sum+float(word_distance_shop_number_row[2])
        x.append(word_distance_shop_number_row[1])
        y.append(shop_number_sum)

    sum_less=0
    for distance_shop_number_row in word_distance_shop_number:
        if distance_shop_number_row[1]<= 200000:
            sum_less=sum_less+distance_shop_number_row[2]
#print 'less than 200000: '+str(sum_less)
#print 'total shop number: '+str(shop_number_sum)
    propotion= round(float(sum_less)/float(shop_number_sum),2)

    avg_distance=avgFind(word_distance_shop_number)
    print 'avg_distance'+str(avg_distance)
    
    isRegional='unknown'
    if int(shop_number_sum) > 15:
        if propotion>=0.6:
            if avg_distance<250000:
                isRegional='true'
            else:
                isRegional='false'
        else:
            isRegional='false'
    output_list.append((word_coor_row['word'],sum_less,int(shop_number_sum),propotion,isRegional))

output_list=sorted(output_list, key=lambda propotion: propotion[3], reverse=True);

true_number=0
false_number=0
unknown_number=0
for out_put_row in output_list:
    if out_put_row[4]=='true':
        true_number=true_number+1
        print out_put_row
    elif out_put_row[4]=='false':
        false_number=false_number+1
        print out_put_row
    else:
        unknown_number=unknown_number+1;

print 'true_number: '+ str(true_number)
print 'false_number: '+ str(false_number)
print 'unknown_number: '+ str(unknown_number)



#if file exist, delete
output_filename = '/Users/mac/Documents/Dissertation/documents/word_ritio_score.csv'
if os.path.exists(output_filename):
    os.remove(output_filename)

#write result into wordLocation.csv
headers = ['word', 'shop_num_less_value','total_shop_num','propotion','regional']
with open(output_filename,'wb') as output_file:
    csvWriter = csv.writer(output_file)
    csvWriter.writerow(headers)
    for data in output_list:
        csvWriter.writerow(data)
output_file.close






