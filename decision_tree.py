import csv
from math import log
import operator

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
                if proportion > 0.7:
                    pro='pro>0.7'
                else:
                    pro='pro<=0.7'
                shopNumber=int(samples['shopNumberLessThanMedian'])+int(samples['shopNumberLargerThanMedian'])
                if shopNumber>10:
                    total_num='shop_num>10'
                else:
                    total_num='shop_num<=10'
            sample_list.append([city_num,avg_dis,pro,total_num,samples['regional']])
        csv_sample_dataset.close


    labels = ['cityNumber','avgDistance','proportion','shopNumber']
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
    classLabel='unknown'
    for key in secondDict.keys():
        
        if testVec[labelIndex]==key:
            
            if type(secondDict[key]).__name__=='dict':
                classLabel=classify(secondDict[key],label,testVec)
            else:
                classLabel=secondDict[key]
    return classLabel

dataSet, labels=createDataset()
tree=createTree(dataSet, labels)
print tree

#testcode
tt = dataSet[39]
print classify(tree,['cityNumber','avgDistance','proportion','shopNumber'],tt)
'''x = classify(tree,tt,labels)
print x'''
