import csv
from math import log
import operator

def
sample_list=[]
with open('/Users/mac/Documents/Dissertation/documents/training_dataset.csv','rb') as csv_sample_dataset:
    reader_sample = csv.DictReader(csv_sample_dataset,delimiter=',')
    for samples in reader_sample:
        if samples['word']!='':
            sample_list.append((samples['word'],samples['cityNumber'],samples['radius'],samples['shopNumberLessThanMedian'],samples['shopNumberLargerThanMedian'],samples['avgDistance'],samples['regional']))
    csv_sample_dataset.close


labels = ['cityNumber','radius','ratio_less_total','avgDistance']

#calculate entropy
def calcShannonEnt(dataSet):
    numEntries=len(dataSet)  # 数据条数
    labelCounts={}
    for featVec in dataSet:
        currentLabel=featVec[-1] # 每行数据的最后一个字（类别）
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1  # 统计有多少个类以及每个类的数量
    shannonEnt=0
    for key in labelCounts:
        prob=float(labelCounts[key])/numEntries # 计算单个类的熵值
        shannonEnt-=prob*log(prob,2) # 累加每个类的熵值
    return shannonEnt
