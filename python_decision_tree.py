from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.externals.six import StringIO
import graphviz
import pydotplus
import sys
import os
from IPython.display import Image
import csv

global feature_data
global feature_judge
feature_data=[]
feature_judge=[]
def createDataset():
    sample_list=[]
        #with open('/Users/mac/Documents/Dissertation/documents/training_dataset.csv','rb') as csv_sample_dataset:
    with open('/Users/mac/Documents/Dissertation/documents/noun_phases_training_dataset.csv','rb') as csv_sample_dataset:
        reader_sample = csv.DictReader(csv_sample_dataset,delimiter=',')
        for samples in reader_sample:
            if samples['word']!='':
                
                proportion=round(float(samples['shopNumberLessThanMedian'])/(float(samples['shopNumberLargerThanMedian'])+float(samples['shopNumberLessThanMedian'])),2)
                
                if proportion > 0.67:
                    pro='pro>0.67'
                    print 'proportion'+str(proportion)
                else:
                    pro='pro<=0.67'
                shopNumber=int(samples['shopNumberLessThanMedian'])+int(samples['shopNumberLargerThanMedian'])
                if shopNumber>10:
                    total_num='shop_num>10'
                else:
                    total_num='shop_num<=10'
            feature_data.append([samples['cityNumber'],float(samples['avgDistance']),proportion,shopNumber,samples['word_ratio']])
            feature_judge.append(samples['regional'])
        csv_sample_dataset.close

createDataset()
#iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(feature_data, feature_judge)
print len(feature_data)
print len(feature_judge)
dot_data=tree.export_graphviz(clf, out_file=None,
                                feature_names=['cityNumber','avgDistance','proportion','shopNumber','ratio'],
                                class_names=['N','Y'],
                                filled=True, rounded=True,
                                special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data)

#graph = graphviz.Source(dot_data)
graph.write_pdf('/Users/mac/Documents/Dissertation/progress/nounPhase_change.pdf')
#Image(graph.create_png())

out_put_list=[]
with open('/Users/mac/Documents/Dissertation/documents/nounPhase_city_small_larger_md_ad.csv','rb') as csv_predict_dataset:
    reader_pre = csv.DictReader(csv_predict_dataset,delimiter=',')
    for samples in reader_pre:
        if samples['word']!='':
            
            proportion=round(float(samples['shopNumberLessThanMedian'])/(float(samples['shopNumberLargerThanMedian'])+float(samples['shopNumberLessThanMedian'])),2)
            
            if proportion > 0.67:
                pro='pro>0.67'
                print 'proportion'+str(proportion)
            else:
                pro='pro<=0.67'
            shopNumber=int(samples['shopNumberLessThanMedian'])+int(samples['shopNumberLargerThanMedian'])
            if shopNumber>10:
                total_num='shop_num>10'
            else:
                total_num='shop_num<=10'
        out_put_list.append([samples['word'],clf.predict([[samples['cityNumber'],float(samples['avgDistance']),proportion,shopNumber,samples['word_ratio']]])[0]])
csv_predict_dataset.close

number_regional=0
regional_nonu_phrases=[]
str_word=''
for output in out_put_list:
    if output[1]=='Y':
        number_regional=number_regional+1
        regional_nonu_phrases.append([output[0],output[1]])
        str_word=str_word+str(output[0])+', '
        print output
print 'number_regional: '+ str(number_regional)
print str_word
output_list=sorted(out_put_list, key=lambda word_judge: word_judge[1])

#if file exist, delete
output_filename = '/Users/mac/Documents/Dissertation/documents/noun_phrase_regional_result.csv'
if os.path.exists(output_filename):
    os.remove(output_filename)

#write result into wordLocation.csv
headers = ['word', 'regional']
with open(output_filename,'wb') as output_file:
    csvWriter = csv.writer(output_file)
    csvWriter.writerow(headers)
    for data in regional_nonu_phrases:
        csvWriter.writerow(data)
output_file.close
