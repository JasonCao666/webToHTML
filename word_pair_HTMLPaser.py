#coding:utf-8
import csv
import re
import sys
import os
import pandas as pd
from HTMLParser import HTMLParser
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import string
import spacy

reload(sys)
sys.setdefaultencoding('utf8')
csv.field_size_limit(500 * 1024 * 1024)

global filted_result_list
filted_result_list=[]
nlp = spacy.load('en')

#remove BOM
def removeBom(file):
    BOM = b'\xef\xbb\xbf'
    existBom = lambda s: True if s==BOM else False
    
    f = open(file, 'rb')
    if existBom( f.read(3) ):
        fbody = f.read()
        with open(file, 'wb') as f:
            f.write(fbody)

def getWordList(file_name):
    words=[]
    with open(file_name,'rb') as csv_regional_word:
        regional_word_input = csv.DictReader(csv_regional_word,delimiter=',')
        for word_input in regional_word_input:
            
            if word_input['word']!='' and word_input['regional']=='Y':
                words.append(word_input['word'])
    csv_regional_word.close
    return words

def loop(input_list):
    path='/Users/mac/Documents/Dissertation/HTML/'
    #path='/Users/mac/Documents/Dissertation/testDocument/HTML/'
    for input_row in input_list:
        with open(path+input_row[2],'rb') as csv_HTML:
            HTML_reader = csv.DictReader(csv_HTML,delimiter=',')
            for HTML_content in HTML_reader:
                parser = MyHTMLParser()
                parser.setIdCoordination(str(input_row[0]),str(input_row[1]))
                parser.feed(str(HTML_content['HTML_content']))

class MyHTMLParser(HTMLParser):
    
    def setIdCoordination(self, id, coordination):
        self.id=id
        self.coordination=coordination
        self.tags=[]
        self.testList=['script', 'style', 'link', 'head', 'a', 'title']
        self.result_row=[]
    
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
    
    
    #print self.tags
    #print("Encountered a start tag:", tag)
    #tags.push(tag)
    #print("Encountered a start tag:", tag)
    
    def handle_endtag(self, tag):
        if len(self.tags) !=0:
            self.tags.pop()
    #print("Encountered a end tag:", tag)

    def handle_data(self, data):
        global filted_result_list
        if len(self.tags)==0:
            return
        if self.tags[-1] in self.testList:
            return
        else:
            handled_row=[]
            re_newline = re.compile('\n')
            re_space = re.compile('\t')
            re_tag_point = re.compile('\'')
            re_HTML_sambols=re.compile(r',|\.|\(|\)|\:|-|–|\"|\+|\'|\!|\?|\*|\>|\%|\{|\}|;|#|\\|\||/')
            re_HTML_numbers=re.compile(r'[0-9]')
            data=re_newline.sub('',data)
            data=re_space.sub('',data)
            data=re_tag_point.sub('',data)
            data=re_HTML_sambols.sub('',data)
            data=re_HTML_numbers.sub('',data)
            data=data.lower()
            data=data.lstrip()
            data=data.rstrip()
            if data!='':
                try:
                    test_doc = nlp(u'%s' % (data))
                    for np in test_doc.noun_chunks:
                        np=str(np).lstrip()
                        np=np.rstrip()
                        if np!='':
                            filted_result_list.append([self.id,self.coordination,np])
                except Exception,err:
                    print err

'''def handle_startendtag(self, tag, attrs):
    
    recognize tag that without endtag, like <img />
    :param tag:
    :param attrs:
    :return:
    print("Encountered startendtag :", tag)'''

'''def handle_comment(self,data):
    :param data:
    :return:
    print("Encountered comment :", data)'''

input_list=[]
input_filename = '/Users/mac/Documents/Dissertation/documents/test_HTML_filename.csv'
#input_filename = '/Users/mac/Documents/Dissertation/testDocument/test_HTML_filename.csv'
removeBom(input_filename)
with open(input_filename,'rb') as csv_input:
    reader_input = csv.DictReader(csv_input,delimiter=',')
    for id_location_website in reader_input:
        input_ids_coordination=[]
        if id_location_website['id']!='' and id_location_website['HTML_file_name']!=-1:
            input_ids_coordination.append(id_location_website['id'])
            input_ids_coordination.append(id_location_website['coordination'])
            input_ids_coordination.append(id_location_website['HTML_file_name'])
            input_list.append(input_ids_coordination)
csv_input.close


loop(input_list)


re_encode=re.compile(r'\\([a-zA-Z0-9]){3}')
filted_result_list =  eval(re_encode.sub('',str(filted_result_list)))

'''for i in range(len(filted_result_list)):
    new_word=''
    if
    filter_doc = nlp(u'%s' % (filted_result_list[i][2]))
    for word in filter_doc:
        if word.pos_ =='NOUN':
            new_word=str(new_word)+str(word)+' '
    new_word=new_word.rstrip()
    filted_result_list[i][2]=new_word'''


#if file exist, delete
output_filename = '/Users/mac/Documents/Dissertation/documents/nounPhaseLocation.csv'
#output_filename = '/Users/mac/Documents/Dissertation/testDocument/wordLocation.csv'
if os.path.exists(output_filename):
    os.remove(output_filename)

#write result into wordLocation.csv
headers = ['id', 'coordination', 'word']
with open(output_filename,'wb') as output_file:
    csvWriter = csv.writer(output_file)
    csvWriter.writerow(headers)
    for data in filted_result_list:
        if data[2]!='' and len(data[2])>2:
            csvWriter.writerow(data)
output_file.close











