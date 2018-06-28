import csv


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
print word_set

word_score_shop_sorted_list=[]
for word in word_set:
    print 'start split'
    word_score_shop_wait_sort=[]
    for word_score_shop in word_score_shop_list:
        if word==word_score_shop[0]:
            word_score_shop_wait_sort.append((word_score_shop[0],word_score_shop[1],word_score_shop[2]))
    #do sort here
    word_score_shop_wait_sort=sorted(word_score_shop_wait_sort, key=lambda sortObject: float(sortObject[1]))
    print word_score_shop_wait_sort


