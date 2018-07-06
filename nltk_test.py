import csv
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

input_list=[]
input_filename = '/Users/mac/Documents/Dissertation/documents/wordLocation.csv'
#input_filename = '/Users/mac/Documents/Dissertation/testDocument/test_HTML_filename.csv'
with open(input_filename,'rb') as csv_input:
    reader_input = csv.DictReader(csv_input,delimiter=',')
    for word_location in reader_input:
        if word_location['word']!='':
            input_list.append(word_location['word'])
csv_input.close


'''for input_list_row in input_list:
    a,b= nltk.pos_tag([input_list_row])[0]
    matchNN = re.match( r'^NN.*', b)
    if matchNN:
        print b'''

example=['chip','chips','chipss','potatoes','potato','haggis']
ps = PorterStemmer()

for input_list_row in example:
    diff=  len(input_list_row)-len(ps.stem(input_list_row))
    print diff
    print nltk.pos_tag([input_list_row])[0]
    a,b= nltk.pos_tag([input_list_row])[0]
   
    matchNN = re.match( r'NNS', b)
    print b
    if diff<3 and matchNN:
        if input_list_row[len(ps.stem(input_list_row)):len(input_list_row)] == 's' or input_list_row[len(ps.stem(input_list_row)):len(input_list_row)]=='es':
            input_list_row=input_list_row[0:len(ps.stem(input_list_row))]
    else:
        print str(len(input_list_row))+' '+str(len(ps.stem(input_list_row)))
        print input_list_row+' '+ps.stem(input_list_row)
        continue
    

#print(input_list_row + ":" + ps.stem(input_list_row))
#print nltk.pos_tag([input_list_row])
#print nltk.pos_tag(input_list_row)

