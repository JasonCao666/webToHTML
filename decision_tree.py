import csv
from math import log
import operator
import os

def createDataset():
    sample_list=[]
    with open('/Users/mac/Documents/Dissertation/documents/training_dataset.csv','rb') as csv_sample_dataset:
        reader_sample = csv.DictReader(csv_sample_dataset,delimiter=',')
        for samples in reader_sample:
            if samples['word']!='':
                if int(samples['cityNumber'])>19:
                    city_num='city>19'
                else:
                    city_num='city<=19'
                if float(samples['avgDistance'])>300000:
                    avg_dis='avg_dis>300000'
                else:
                    avg_dis='avg_dis<=300000'
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
                if float(samples['word_ratio'])>=0.65:
                    shop_ratio='shop_ratio>=0.65'
                else:
                    shop_ratio='shop_ratio<0.65'
            sample_list.append([city_num,avg_dis,pro,total_num,shop_ratio, samples['regional']])
        csv_sample_dataset.close


    labels = ['cityNumber','avgDistance','proportion','shopNumber','shop_ratio']
    return sample_list,labels

#calculate entropy
def calcShannonEnt(dataSet):
    numEntries=len(dataSet)
    labelCounts={}
    for featVec in dataSet:
        currentLabel=featVec[-1]
        #print 'currentLabel: '+str(currentLabel)
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1
    shannonEnt=0
    for key in labelCounts:
        prob=float(labelCounts[key])/numEntries
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

def splitDataSet(dataSet,axis,value):
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFeatVec =featVec[:axis]
            print 'reducedFeatVec: '+str(reducedFeatVec)
            reducedFeatVec.extend(featVec[axis+1:])
            print 'reducedFeatVec after extent: '+str(reducedFeatVec)
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0])-1
    print 'numFeatures: '+str(numFeatures)
    baseEntropy = calcShannonEnt(dataSet)
    print 'baseEntropy: '+str(baseEntropy)
    bestInfoGain = 0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        print 'featList: '+str(featList)
        uniqueVals = set(featList)
        newEntropy = 0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            print 'subDataSet: '+str(subDataSet)
            prob =len(subDataSet)/float(len(dataSet))
            newEntropy +=prob*calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        print 'infoGain: '+str(infoGain)
        if (infoGain>bestInfoGain):
            bestInfoGain=infoGain
            bestFeature = i
        print 'bestFeature: '+str(bestFeature)
    return bestFeature

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]
    print 'classList'+str(classList)
    if classList.count(classList[0])==len(classList):
        return classList[0]
    if len(dataSet[0])==1:
        return majorityCnt(classList)
    print 'dataset: '+str(dataSet)
    bestFeat=chooseBestFeatureToSplit(dataSet)
    bestFeatLabel=labels[bestFeat]
    myTree={bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues=[example[bestFeat] for example in dataSet]
    print 'Best featValues: '+str(featValues)
    uniqueVals=set(featValues)
    for value in uniqueVals:
        subLabels=labels[:]
        myTree[bestFeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

def classify(tree,label,testVec):
    firstFeat=tree.keys()[0]
    secondDict=tree[firstFeat]
    labelIndex=label.index(firstFeat)
    classLabel='N'
    for key in secondDict.keys():
        if testVec[labelIndex]==key:
            if type(secondDict[key]).__name__=='dict':
                classLabel=classify(secondDict[key],label,testVec)
            else:
                classLabel=secondDict[key]
    return classLabel

dataSet, labels=createDataset()
tree=createTree(dataSet, labels)



#testcode
testdata_dict={}
with open('/Users/mac/Documents/Dissertation/documents/word_city_small_larger_md_ad.csv','rb') as csv_test_file:
    reader_test_dataset = csv.DictReader(csv_test_file,delimiter=',')
    for test_row in reader_test_dataset:
        testdata_list=[]
        if test_row['word']!='':
            if int(test_row['cityNumber'])>19:
                city_num='city>19'
            else:
                city_num='city<=19'
            if float(test_row['avgDistance'])>300000:
                avg_dis='avg_dis>300000'
            else:
                avg_dis='avg_dis<=300000'
            proportion=round(float(test_row['shopNumberLessThanMedian'])/(float(test_row['shopNumberLargerThanMedian'])+float(test_row['shopNumberLessThanMedian'])),2)
            if proportion > 0.67:
                pro='pro>0.67'
            else:
                pro='pro<=0.67'
            shopNumber=int(test_row['shopNumberLessThanMedian'])+int(test_row['shopNumberLargerThanMedian'])
            if shopNumber>10:
                total_num='shop_num>10'
            else:
                total_num='shop_num<=10'
            if float(test_row['word_ratio'])>=0.65:
                shop_ratio='shop_ratio>=0.65'
            else:
                shop_ratio='shop_ratio<0.65'
            testdata_list.append([city_num,avg_dis,pro,total_num,shop_ratio])
            testdata_dict[test_row['word']]=testdata_list
    csv_test_file.close

output_list=[]
for key in testdata_dict:
    output_list.append((key,classify(tree,['cityNumber','avgDistance','proportion','shopNumber','shop_ratio'],testdata_dict[key][0])))

output_list=sorted(output_list, key=lambda word_judge: word_judge[1])

regional_word_num=0
wide_word_num=0
unknown_word_num=0
for output_row in output_list:
    if output_row[1]=='Y':
        regional_word_num=regional_word_num+1
        print output_row[0]
    elif output_row[1]=='N':
        wide_word_num=wide_word_num+1
        print output_row
    else:
        unknown_word_num=unknown_word_num+1
print 'regional_word_num'+str(regional_word_num)
print 'wide_word_num'+str(wide_word_num)
print 'unknown_word_num'+str(unknown_word_num)

print tree
'''tt = dataSet[39] )
print classify(tree,['cityNumber','avgDistance','proportion','shopNumber'],tt)
x = classify(tree,tt,labels)
print x'''

#if file exist, delete
output_filename = '/Users/mac/Documents/Dissertation/documents/regional_result_ratio.csv'
if os.path.exists(output_filename):
    os.remove(output_filename)

#write result into wordLocation.csv
headers = ['word', 'regional']
with open(output_filename,'wb') as output_file:
    csvWriter = csv.writer(output_file)
    csvWriter.writerow(headers)
    for data in output_list:
        csvWriter.writerow(data)
output_file.close

