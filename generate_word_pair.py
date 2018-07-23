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
import itertools

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
    
    def handle_endtag(self, tag):
        if len(self.tags) !=0:
            self.tags.pop()

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
            re_HTML_numbers=re.compile(r'[0-9]')
            re_HTML_tag1=re.compile(r'^.*£.*$')
            re_HTML_sambols=re.compile(r',|\.|\(|\)|\:|-|–|\"|\+|\'|\!|\?|\*|\>|\%|\{|\}|;|#|\\|\||&')
            re_HTML_sambol1=re.compile(r'\/')
            re_HTML_tag2=re.compile(r'^.*@.*$')
            re_HTML_tag3=re.compile(r'^.*www.*$')
            
            data=re_newline.sub('',data)
            data=re_space.sub('',data)
            data=re_HTML_numbers.sub('',data)
            data=re_HTML_tag1.sub('',data)
            data=re_HTML_tag2.sub('',data)
            data=re_HTML_tag3.sub('',data)
            data=re_HTML_sambols.sub(' ',data)
            data=re_HTML_sambol1.sub(' ',data)
            data=data.lower()
            data=data.lstrip()
            data=data.rstrip()
            
            if data!='':
                pairs=data.split()
                if len(pairs)==1:
                    word_pair=pairs[0]
                    filted_result_list.append([self.id, self.coordination, word_pair])
                elif len(pairs)==2:
                    for i in range(len(pairs)):
                        if i!=len(pairs)-1:
                            word_pair=str(pairs[i])+' '+str(pairs[i+1])
                            filted_result_list.append([self.id, self.coordination, word_pair])
                            break
                else:
                    for i in range(len(pairs)):
                        if i!=len(pairs)-1:
                            word_pair=str(pairs[i])+' '+str(pairs[i+1])
                            filted_result_list.append([self.id, self.coordination, word_pair])





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


#if file exist, delete
output_filename = '/Users/mac/Documents/Dissertation/documents/word_pair_Location.csv'
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












