#coding:utf-8
import csv
import re
import sys
import os
import pandas as pd
from HTMLParser import HTMLParser
import nltk
reload(sys)
sys.setdefaultencoding('utf8')
csv.field_size_limit(500 * 1024 * 1024)

global filted_result_list
filted_result_list=[]

#remove BOM
def removeBom(file):
    BOM = b'\xef\xbb\xbf'
    existBom = lambda s: True if s==BOM else False
    
    f = open(file, 'rb')
    if existBom( f.read(3) ):
        fbody = f.read()
        with open(file, 'wb') as f:
            f.write(fbody)


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
        if len(self.tags)==0:
            return
        if self.tags[-1] in self.testList:
            return
        else:
            global filted_result_list
            #print 'tagname: '+self.tags[-1]
            re_newline = re.compile('\n')
            re_space = re.compile('\t')
            re_HTML_numbers=re.compile(r'[0-9]')
            re_HTML_tag1=re.compile(r'^.*£.*$')
            re_HTML_sambols=re.compile(r',|\.|\(|\)|\:|-|–|\"|\+|\'|\!|\?|\*|\>|\%|\{|\}|;|#|\\|\|')
            re_HTML_sambol1=re.compile(r'\/')
            re_HTML_tag2=re.compile(r'^.*@.*$')
            re_HTML_tag3=re.compile(r'^.*www.*$')
            
            data=re_HTML_numbers.sub('',data)
            data=re_HTML_tag1.sub('',data)
            data=re_HTML_tag2.sub('',data)
            data=re_HTML_tag3.sub('',data)
            data=re_HTML_sambols.sub(' ',data)
            data=re_HTML_sambol1.sub(' ',data)
            data=re_newline.sub('',data)
            data=re_space.sub('',data)
            
            split_result=data.split()
            for j in range(len(split_result)):
                self.result_row=[]
                
                if len(split_result[j])>1 and split_result[j]!=' ':
                    re_HTML_space1=re.compile(r'​​')
                    '''re_HTML_connectors=re.compile(r'^and$|^or$|^with$|^the$|^to$|^of$|^in$|^is$|^if$|^by$|^pm$|^am$|^from$|^for$|^between$|^day$|^with$|^opening$|^open$|only|^see$|^still$|^order$|^orders$|^on$|^as$|^at$|^brfore$|^be$|^are$|^take$|^away$|^get$|^can$|^but$|^an$|^any$|^about$|^all$|^when$|^has$|^more$|^lots$|^also$|^new$|^may$|^vary$|^maybe$')
                    re_HTML_personal=re.compile(r'^you$|^your$|^we$|^our$|^this$|^that$|^other$|^please$|^own$|^it$|^its$|^us$|^there$|^here$')
                    re_HTML_verbs=re.compile(r'^come$|^hear$|^been$|^selected$|^wish$|^buy$|^like$|^closing$|^helps$|^follows$|^find$|^starting$|^forget$|^serves$|^cancel$|^takeway$|^did$')'''
                    
                    split_result[j]=split_result[j].lower()
                    split_result[j]=re_HTML_space1.sub('',split_result[j])
                    '''split_result[j]=re_HTML_connectors.sub('',split_result[j])
                    split_result[j]=re_HTML_personal.sub('',split_result[j])'''
                    
                    
                    
                    if split_result[j]!='':
                        
                        self.result_row.append(self.id)
                        self.result_row.append(self.coordination)
                        #print filted_split_result
                        self.result_row.append(split_result[j])
                        '''self.result_row.append(str(split_result[j]).replace('\xc2\xa0', '').replace('\xe2\x80\xa6', ' ').replace('\xf0\x9f\xa4\x97','').replace('\xe2\x80\x8b','').replace('\xc2\xa9','').replace('\xc3\xabt','').replace('\xc3\xa9ed','').replace('\xe2\x80\x99re','').replace('\xe2\x80\x99ll','').replace('\xe2\x80\x99s','').replace('\xe2\x80\x9d','').replace('\xc3\xb1os','').replace('\xc3\xb1o','').replace('\xe2\x80\x9ci','').replace('\xc3\xa4agen','').replace('\xf0\x9f\x91\x8d\xf0\x9f\x8f\xbb','').replace('\xe2\x80\x98n\xe2\x80\x99','').replace('\xc2\xa3','').replace('\xf1os','').replace('\xe2\x80\x99ve','').replace('\xf0\x9f\x92\xaa','').replace('\xc3\x97','').replace('\xc5\x82','').replace('\xf0\x9f\x8d\xbd\xf0\x9f\x90\x9f\xf0\x9f\x8d\x9f\xf0\x9f\x8d\x9e\xf0\x9f\x8d\x97','').replace('\xf0\x9f\x98\x81\xe2\x98\x8e\xef\xb8\x8f\xf0\x9f\x93\xb2','').replace('\xef\xbb\xbf','').replace('\xc3\xa9','').replace('\xc2\xbd','').replace('\xc3\x89','').replace('\xe2\x80\x99','').replace('\xe2\x80\x9c','').replace('\xc2\xbc','').replace('\xe9','').replace('\xc3\xaf\xc2\xbf','').replace('\x03\x03','').replace('\xf0\x9f\x91\x8d','').replace('\xef\x82\x95','').replace('\xe2\x80\x98','').replace('\xe2\x98\x86\xe2\x98\x86\xe2\x98\x86\xe2\x98\x86\xe2\x98\x86','').replace('\xa0\xa0','').replace('\xe2\x80\xa2','').replace('\xa0','').replace('\xe2\x96\xbc','').replace('\xc2\xbb','').replace('\xe2\x80\x94','').replace('\xf0\x9f\x91\x8c\xf0\x9f\x91\x8c','').replace('\xc3\xa8','').replace('\x03','').replace('\xe2\x98\xba',''))'''
                        filted_result_list.append(self.result_row)

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

path='/Users/mac/Documents/Dissertation/HTML/'
#path='/Users/mac/Documents/Dissertation/testDocument/HTML/'
for input_row in input_list:
    with open(path+input_row[2],'rb') as csv_HTML:
        HTML_reader = csv.DictReader(csv_HTML,delimiter=',')
        for HTML_content in HTML_reader:
            parser = MyHTMLParser()
            parser.setIdCoordination(str(input_row[0]),str(input_row[1]))
            parser.feed(str(HTML_content['HTML_content']))

re_encode=re.compile(r'\\([a-zA-Z0-9]){3}')  
filted_result_list =  eval(re_encode.sub('',str(filted_result_list)))
for i in range(len(filted_result_list)):
    if filted_result_list[i][2]!='':
        a,b= nltk.pos_tag([filted_result_list[i][2]])[0]
        matchNN = re.match( r'^NN.*', b)
        if matchNN:
            continue
        else:
            filted_result_list[i][2]=''
#print type(re_encode.sub('',str(filted_result_list)))
#print re_encode.sub('',str(filted_result_list))

#if file exist, delete
output_filename = '/Users/mac/Documents/Dissertation/documents/wordLocation.csv'
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
            if data[0] == '196':
                print data
            csvWriter.writerow(data)
output_file.close


