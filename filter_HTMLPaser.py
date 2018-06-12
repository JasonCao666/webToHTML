
import csv
import re
import sys
import os
import pandas as pd
from HTMLParser import HTMLParser
reload(sys)
sys.setdefaultencoding("utf-8")
csv.field_size_limit(500 * 1024 * 1024)

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
    
    def handle_starttag(self, tag, attrs):
        if tag!='script' and tag!='head' and tag!='link' and tag!='p' and tag!='meta' and tag!='style' and tag!='a':
            print("Encountered a start tag:", tag)

    def handle_data(self, data):
        if len(data)<100 and len(data)>1:
            print("Encountered some data  :", data)
            return data
    
    def handle_endtag(self, tag):
        if tag!='script' and tag!='head' and tag!='link' and tag!='p' and tag!='meta' and tag!='style' and tag!='a':
            print("Encountered a end tag:", tag)
    
    
    
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

parser = MyHTMLParser()
filted_result_list=[]
path='/Users/mac/Documents/Dissertation/HTML/'
for input_row in input_list:
    filter_result=[]
    filter_result.append(input_row[0])
    filter_result.append(input_row[1])
    with open(path+input_row[2],'rb') as csv_HTML:
        HTML_reader = csv.DictReader(csv_HTML,delimiter=',')
        for HTML_content in HTML_reader:
            print parser.feed(str(HTML_content['HTML_content']))



