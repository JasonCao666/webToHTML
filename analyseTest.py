import csv

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
    print '-------------'+str(raw_list[0][0])+' test---------------'
    distances=[]
    for row in raw_list:
        distances.append(float(row[1]))
    print distances
    median_distance = medianFind(distances)
    median_small_shops=0
    median_larger_shops=0
    for row in raw_list:
        if float(row[1])<median_distance:
            median_small_shops=median_small_shops+int(row[2])
        else:
            median_larger_shops=median_larger_shops+int(row[2])

    print 'total city '+str(len(raw_list))
    print 'shop small '+str(median_small_shops)
    print 'shop larger '+str(median_larger_shops)
    print 'max distance '+ str(max(distances))
    print 'avg distance '+ str(avgFind(distances))




#read word, coordination file and save values in the list
word_score_shop_list=[]
with open('/Users/mac/Documents/Dissertation/documents/word_score_shop.csv','rb') as csv_word_score_shop:
    reader_word_score_shop = csv.DictReader(csv_word_score_shop,delimiter=',')
    for word_score_shop in reader_word_score_shop:
        word_score_shop_dict=[]
        if word_score_shop['word']!='':
            word_score_shop_dict.append(word_score_shop['word'])
            word_score_shop_dict.append(word_score_shop['score'])
            word_score_shop_dict.append(word_score_shop['shop_number'])
            word_score_shop_list.append(word_score_shop_dict)
    csv_word_score_shop.close

#print word_score_shop_list

total_word_list=[]
for word_score_shop in word_score_shop_list:
    total_word_list.append(word_score_shop[0])

word_set=set(total_word_list)

'''word_score_shop_sorted_list=[]
for word in word_set:
    print 'start split'
    word_score_shop_wait_sort=[]
    for word_score_shop in word_score_shop_list:
        if word==word_score_shop[0]:
            word_score_shop_wait_sort.append((word_score_shop[0],word_score_shop[1],word_score_shop[2]))
    #do sort here
    word_score_shop_wait_sort=sorted(word_score_shop_wait_sort, key=lambda sortObject: float(sortObject[1]))
    print word_score_shop_wait_sort
    if word_score_shop_wait_sort[0][0] =='fishcake':
        chip_word_score_shop_sorted_list=word_score_shop_wait_sort

print chip_word_score_shop_sorted_list'''

chip_word_score_shop_sorted_list=[('chips', '42723.7', '9'), ('chips', '54357.1', '8'), ('chips', '76452.55', '13'), ('chips', '101159.32', '5'), ('chips', '103598.15', '7'), ('chips', '131049.51', '1'), ('chips', '131325.43', '7'), ('chips', '184099.11', '12'), ('chips', '191001.36', '3'), ('chips', '197377.54', '2'), ('chips', '209593.5', '4'), ('chips', '214968.62', '6'), ('chips', '230042.23', '11'), ('chips', '232463.16', '8'), ('chips', '239074.06', '4'), ('chips', '246210.18', '4'), ('chips', '250439.24', '9'), ('chips', '253442.94', '5'), ('chips', '302424.45', '4'), ('chips', '380977.78', '2'), ('chips', '414634.58', '5'), ('chips', '421836.73', '9'), ('chips', '428224.98', '2'), ('chips', '429594.51', '4'), ('chips', '438266.73', '2'), ('chips', '445122.4', '9'), ('chips', '446630.02', '14'), ('chips', '466629.3', '12'), ('chips', '473714.0', '15'), ('chips', '482971.4', '3'), ('chips', '543132.6', '6'), ('chips', '562082.74', '2'), ('chips', '584533.53', '3')]
calculateOpt(chip_word_score_shop_sorted_list)

haggis_word_score_shop_sorted_list=[('haggis', '73245.15', '14'), ('haggis', '108197.13', '4'), ('haggis', '127995.56', '15'), ('haggis', '138288.05', '4'), ('haggis', '158218.66', '4'), ('haggis', '178704.22', '6'), ('haggis', '185946.92', '3'), ('haggis', '214699.88', '4'), ('haggis', '240510.43', '4'), ('haggis', '243535.71', '2'), ('haggis', '248490.07', '1'), ('haggis', '337582.55', '1')]
calculateOpt(haggis_word_score_shop_sorted_list)

fishcake_word_score_shop_sorted_list=[('fishcake', '10923.06', '5'), ('fishcake', '107161.52', '1'), ('fishcake', '114147.36', '3'), ('fishcake', '126373.22', '3'), ('fishcake', '140147.91', '1'), ('fishcake', '145183.26', '2'), ('fishcake', '157558.23', '3'), ('fishcake', '167818.3', '4'), ('fishcake', '284590.27', '3'), ('fishcake', '295373.62', '3'), ('fishcake', '306165.15', '1'), ('fishcake', '313112.11', '1'), ('fishcake', '362860.12', '1'), ('fishcake', '365292.63', '2'), ('fishcake', '378666.86', '1'), ('fishcake', '403276.53', '1'), ('fishcake', '417110.35', '1'), ('fishcake', '475798.68', '1'), ('fishcake', '502424.57', '1'), ('fishcake', '515687.1', '2'), ('fishcake', '572352.95', '2'), ('fishcake', '588519.52', '2'), ('fishcake', '598080.27', '2'), ('fishcake', '671077.17', '1')]
calculateOpt(fishcake_word_score_shop_sorted_list)





