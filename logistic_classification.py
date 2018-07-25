import matplotlib.pyplot as plt
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn import datasets
import csv
import os


global feature_data
global feature_judge
feature_data=[]
feature_judge=[]
with open('/Users/mac/Documents/Dissertation/documents/noun_phases_training_dataset.csv','rb') as csv_sample_dataset:
    reader_sample = csv.DictReader(csv_sample_dataset,delimiter=',')
    for samples in reader_sample:
        if samples['word']!='':
            
            proportion=round(float(samples['shopNumberLessThanMedian'])/(float(samples['shopNumberLargerThanMedian'])+float(samples['shopNumberLessThanMedian'])),2)
            
            if proportion > 0.67:
                pro='pro>0.67'
            else:
                pro='pro<=0.67'
            shopNumber=int(samples['shopNumberLessThanMedian'])+int(samples['shopNumberLargerThanMedian'])
            if shopNumber>10:
                feature_data.append([float(samples['avgDistance']),proportion,shopNumber,float(samples['word_ratio'])])
                feature_judge.append(samples['regional'])
csv_sample_dataset.close

predict_list_word=[]
predict_list_features=[]
with open('/Users/mac/Documents/Dissertation/documents/nounPhase_city_small_larger_md_ad.csv','rb') as csv_predict_dataset:
    reader_pre = csv.DictReader(csv_predict_dataset,delimiter=',')
    for samples in reader_pre:
        if samples['word']!='':
            
            proportion=round(float(samples['shopNumberLessThanMedian'])/(float(samples['shopNumberLargerThanMedian'])+float(samples['shopNumberLessThanMedian'])),2)
            
            if proportion > 0.67:
                pro='pro>0.67'
            else:
                pro='pro<=0.67'
            shopNumber=int(samples['shopNumberLessThanMedian'])+int(samples['shopNumberLargerThanMedian'])
            if shopNumber>10:
                predict_list_word.append(samples['word'])
                predict_list_features.append([float(samples['avgDistance']),proportion,shopNumber,float(samples['word_ratio'])])
csv_predict_dataset.close
'''iris = datasets.load_iris()
X = iris.data[:, 0:2]  # we only take the first two features for visualization
y = iris.target
print y
print type(y)'''
np_feature_judge=np.array(feature_judge)

n_features = 4
C = 1.0
# Create different classifiers. The logistic regression cannot do
# multiclass out of the box.
classifiers = {'L1 logistic': LogisticRegression(C=C, penalty='l1'),
}

n_classifiers = len(classifiers)
predict_list_features=np.array(predict_list_features).astype(np.float64)

for index, (name, classifier) in enumerate(classifiers.items()):
    classifier.fit(feature_data, np_feature_judge)
    y_pred = classifier.predict(feature_data)
    classif_rate = np.mean(y_pred.ravel() == np_feature_judge.ravel()) * 100
    print("classif_rate for %s : %f " % (name, classif_rate))
    probas = classifier.predict_proba(predict_list_features)

probas=probas.tolist()
output_list=[]
for i in range(len(predict_list_word)):
    output_list.append([predict_list_word[i],probas[i]])
    

output_list=sorted(output_list, key=lambda sortObject: float(sortObject[1][1]), reverse=True)

#if file exist, delete
output_filename = '/Users/mac/Documents/Dissertation/documents/noun_phrase_pro_logistic_result.csv'
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
