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
import time, threading

reload(sys)
sys.setdefaultencoding('utf8')
csv.field_size_limit(500 * 1024 * 1024)

global context_result_list
context_result_list=[]

#remove BOM
def removeBom(file):
    BOM = b'\xef\xbb\xbf'
    existBom = lambda s: True if s==BOM else False
    
    f = open(file, 'rb')
    if existBom( f.read(3) ):
        fbody = f.read()
        with open(file, 'wb') as f:
            f.write(fbody)

def removePlural(pluralp_data):
    #print 'chips_before: '+ str(pluralp_data)
    ps = PorterStemmer()
    diff=  len(pluralp_data)-len(ps.stem(pluralp_data))
    a,b= nltk.pos_tag([pluralp_data])[0]
    matchNN = re.match( r'NNS', b)
    if diff<3 and matchNN:
        if pluralp_data[len(ps.stem(pluralp_data)):len(pluralp_data)] == 's' or pluralp_data[len(ps.stem(pluralp_data)):len(pluralp_data)]=='es':
            pluralp_data=pluralp_data[0:len(ps.stem(pluralp_data))]
#print 'chips_after: '+ str(pluralp_data)
    return pluralp_data

def getWordList(file_name):
    words=[]
    with open(file_name,'rb') as csv_regional_word:
        regional_word_input = csv.DictReader(csv_regional_word,delimiter=',')
        for word_input in regional_word_input:
            
            if word_input['word']!='' and word_input['regional']=='Y':
                words.append(word_input['word'])
    csv_regional_word.close
    return words

def loop(start,stop,word):
    path='/Users/mac/Documents/Dissertation/HTML/'
    #path='/Users/mac/Documents/Dissertation/testDocument/HTML/'
    for index in range(start,stop):
        with open(path+str(index)+'.csv','rb') as csv_HTML:
            HTML_reader = csv.DictReader(csv_HTML,delimiter=',')
            for HTML_content in HTML_reader:
                #if str(input_row[0])=='87':
                parser = MyHTMLParser()
                parser.setIdCoordination(index,word)
                parser.feed(str(HTML_content['HTML_content']))
        csv_HTML.close

class MyHTMLParser(HTMLParser):
    
    def setIdCoordination(self, id,word):
        self.id=id
        self.tags=[]
        self.testList=['script', 'style', 'link', 'head', 'a', 'title']
        self.result_row=[]
        self.current_tag=''
        self.current_attrs=[]
        self.word=word
    
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        self.current_tag=tag
        self.current_attrs=attrs
    
    #print self.tags
    #print("Encountered a start tag:", tag)
    #tags.push(tag)
    #print("Encountered a start tag:", tag)
    
    def handle_endtag(self, tag):
        if len(self.tags) !=0:
            self.tags.pop()
    #print("Encountered a end tag:", tag)

    def handle_data(self, data):
        global context_result_list
        if len(self.tags)==0:
            return
        if self.tags[-1] in self.testList:
            return
        else:
            handled_row=[]
            re_newline = re.compile('\n')
            re_space = re.compile('\t')
            re_tag_point = re.compile('\'')
            data=re_newline.sub('',data)
            data=re_space.sub('',data)
            data=re_tag_point.sub('',data)
            data=data.lower()
            #and string.find(data,st)!=-1
            data=data.lstrip()
            data=data.rstrip()
            if data.isspace()==False and data!='' and string.find(data,self.word)!=-1:
                #data=removePlural(data)
                #print 'self.current_tag: '+self.current_tag
                handled_row.append(self.word)
                handled_row.append(data)
                handled_row.append(self.id)
                context_result_list.append(handled_row)

#if tags.tail() in ['sctipt', 'style' ...]:
#return
#print("Encountered some data  :", data)

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

#regional_word_filename='/Users/mac/Documents/Dissertation/documents/regional_result.csv'
regional_word_filename='/Users/mac/Documents/Dissertation/documents/noun_phrase_context_input.csv'
words=getWordList(regional_word_filename)

for word in words:
    threads = []
    current_num=1
    for i in range(0,4):
        if i!=3:
            threads.append(threading.Thread(target=loop, args=(current_num,current_num+len(input_list)/4, word), name='LoopThread'))
            current_num=current_num+len(input_list)/4
        elif i==3:
            threads.append(threading.Thread(target=loop, args=(current_num,len(input_list),word), name='LoopThread'))
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

#print context_result_list

'''f_word_context_list = open('/Users/mac/Documents/Dissertation/documents/word_context_list.txt')
word_context_list = f_word_context_list.read()
f_word_context_list.close

re_tag1=re.compile(r'"')
word_context_list=re_tag1.sub('',word_context_list)

re_encode=re.compile(r'\\([a-zA-Z0-9]){3}')
word_context_list=re_encode.sub('',word_context_list)

re_newline = re.compile('\n')
word_context_list=re_newline.sub('',word_context_list)

word_context_list = eval(word_context_list)'''

#if file exist, delete
output_filename = '/Users/mac/Documents/Dissertation/documents/noun_phrase_word_context.csv'
if os.path.exists(output_filename):
    os.remove(output_filename)

#write result into wordLocation.csv
headers = ['word', 'context', 'shop_id']
with open(output_filename,'wb') as output_file:
    csvWriter = csv.writer(output_file)
    csvWriter.writerow(headers)
    for data in context_result_list:
        csvWriter.writerow(data)
output_file.close

