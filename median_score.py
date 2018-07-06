import csv

word_feature_list=[]
with open('/Users/mac/Documents/Dissertation/documents/word_city_small_larger_md_ad.csv','rb') as csv_word_features:
    reader_word_features = csv.DictReader(csv_word_features,delimiter=',')
    for word_feature in reader_word_features:
        if word_feature['word']!='':
           median_propotion=round(float(word_feature['shopNumberLessThanMedian'])/(float(word_feature['shopNumberLargerThanMedian'])+float(word_feature['shopNumberLessThanMedian'])),2)
        word_feature_list.append((word_feature['word'], median_propotion))
    csv_word_features.close

word_feature_list=sorted(word_feature_list, key=lambda word_feature: word_feature[1], reverse = True)


word_feature_list


