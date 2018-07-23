import csv
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import spacy
import itertools

'''input_list=[]
input_filename = '/Users/mac/Documents/Dissertation/documents/wordLocation.csv'
#input_filename = '/Users/mac/Documents/Dissertation/testDocument/test_HTML_filename.csv'
with open(input_filename,'rb') as csv_input:
    reader_input = csv.DictReader(csv_input,delimiter=',')
    for word_location in reader_input:
        if word_location['word']!='':
            input_list.append(word_location['word'])
csv_input.close'''


'''for input_list_row in input_list:
    a,b= nltk.pos_tag([input_list_row])[0]
    matchNN = re.match( r'^NN.*', b)
    if matchNN:
        print b'''

'''example=['chip','chips','chipss','potatoes','potato','haggis']
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
        continue'''
    

#print(input_list_row + ":" + ps.stem(input_list_row))
#print nltk.pos_tag([input_list_row])
#print nltk.pos_tag(input_list_row)

'''nlp = spacy.load('en')
string_doc='Natural language processing (NLP) deals with the application of computational models to text or speech data. Application areas within NLP include automatic (machine) translation between languages; dialogue systems, which allow a human to interact with a machine using natural language; and information extraction, where the goal is to transform unstructured text into structured (database) representations that can be searched and browsed in flexible ways. NLP technologies are having a dramatic impact on the way people interact with computers, on the way people interact with each other through the use of language, and on the way people access the vast amount of linguistic data now in electronic form. From a scientific viewpoint, NLP involves fundamental questions of how to structure formal models (for example statistical models) of natural language phenomena, and of how to design algorithms that implement these models.'

test_doc = nlp(u'%s' % (string_doc))
test_doc2=nlp(u'a splash')
for np in test_doc2.noun_chunks:
    print np

new_word=''
for w in test_doc2:
    print w
    print w.pos
    print w.pos_
    if w.pos_ =='NOUN':
            new_word=str(new_word)+str(w)+' '
new_word=new_word.rstrip()
print new_word'''


'''all_tags = {w.pos: w.pos_ for w in test_doc2}
print all_tags'''

'''nlp = spacy.load('en')
doc1 = nlp(u'chicken wrap')
doc2 = nlp(u'a inch chicken tikk')
print doc1.similarity(doc2)'''

words = ["mama", "papa", "sister", "brother"]
if len(words)==1:
    print words
elif len(words)==2:
    for i in range(len(words)):
        if i!=len(words)-1:
            print str(words[i])+' '+words[i+1]
            break
else:
    for i in range(len(words)):
        if i!=len(words)-1:
            print str(words[i])+' '+words[i+1]

'''pairs = list(itertools.product(words, repeat=2))
print pairs'''

