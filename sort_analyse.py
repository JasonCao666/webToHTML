import csv
import os
global output_list
output_list=[]

def medianFind(lst):
    half = len(lst)//2
    median = (float(lst[half])+float(lst[~half]))/2
    return median

def avgFind(lst):
    b=len(lst)
    sum=0
    for i in lst:
        sum=sum+float(i)
    return sum/b

def calculateOpt(raw_list):
    distances=[]
    for row in raw_list:
        distances.append(float(row[1]))
    median_distance = medianFind(distances)
    median_small_shops=0
    median_larger_shops=0
    for row in raw_list:
        if float(row[1])<median_distance:
            median_small_shops=median_small_shops+int(row[2])
        else:
            median_larger_shops=median_larger_shops+int(row[2])
    output_list.append((row[0],len(raw_list),row[3],row[4],row[5],round(float(median_distance),2),median_small_shops,median_larger_shops,max(distances),round(avgFind(distances),2),row[6]))
    '''print 'total city '+str(len(raw_list))
    print 'shop small '+str(median_small_shops)
    print 'shop larger '+str(median_larger_shops)
    print 'max distance '+ str(max(distances))
    print 'avg distance '+ str(avgFind(distances))'''

#read word, coordination file and save values in the list
word_score_shop_list=[]
with open('/Users/mac/Documents/Dissertation/documents/word_score_shop.csv','rb') as csv_word_score_shop:
    reader_word_score_shop = csv.DictReader(csv_word_score_shop,delimiter=',')
    for word_score_shop in reader_word_score_shop:
        word_score_shop_dict=[]
        if word_score_shop['word']!='':
            word_score_shop_dict.append(word_score_shop['word'])
            word_score_shop_dict.append(word_score_shop['distance_centre'])
            word_score_shop_dict.append(word_score_shop['shop_number'])
            word_score_shop_dict.append(word_score_shop['word_central_lon'])
            word_score_shop_dict.append(word_score_shop['word_central_lat'])
            word_score_shop_dict.append(word_score_shop['radius'])
            word_score_shop_dict.append(word_score_shop['word_ratio'])
            word_score_shop_list.append(word_score_shop_dict)
    csv_word_score_shop.close

#print word_score_shop_list

total_word_list=[]
for word_score_shop in word_score_shop_list:
    total_word_list.append(word_score_shop[0])

word_set=set(total_word_list)
print word_set


#Sort the same words
word_score_shop_sorted_list=[]
for word in word_set:
    print 'start split'
    word_score_shop_wait_sort=[]
    for word_score_shop in word_score_shop_list:
        if word==word_score_shop[0]:
            word_score_shop_wait_sort.append((word_score_shop[0],word_score_shop[1],word_score_shop[2],word_score_shop[3],word_score_shop[4],word_score_shop[5],word_score_shop[6]))
    #do sort here
    word_score_shop_wait_sort=sorted(word_score_shop_wait_sort, key=lambda sortObject: float(sortObject[1]))
    print word_score_shop_wait_sort
    calculateOpt(word_score_shop_wait_sort)


output_list = sorted(output_list, key=lambda output: output[1], reverse = True)

#if file exist, delete
output_filename = '/Users/mac/Documents/Dissertation/documents/word_city_small_larger_md_ad.csv'
if os.path.exists(output_filename):
    os.remove(output_filename)

#write result into wordLocation.csv
headers = ['word', 'cityNumber', 'word_central_lon', 'word_central_lat','radius', 'median' ,'shopNumberLessThanMedian','shopNumberLargerThanMedian','largestDistance','avgDistance','word_ratio']
with open(output_filename,'wb') as output_file:
    csvWriter = csv.writer(output_file)
    csvWriter.writerow(headers)
    for data in output_list:
        csvWriter.writerow(data)
output_file.close
