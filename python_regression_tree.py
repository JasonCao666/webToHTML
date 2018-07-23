import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
import csv

global feature_data
global feature_judge
feature_data=[]
feature_judge=[]

iris = load_iris()
for pairidx, pair in enumerate([[0, 1], [0, 2], [0, 3],
                                [1, 2], [1, 3], [2, 3]]):
    print iris.data[:, pair]

print iris.data
'''def createDataset():
    sample_list=[]
    with open('/Users/mac/Documents/Dissertation/documents/training_dataset.csv','rb') as csv_sample_dataset:
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
        csv_sample_dataset.close'''
