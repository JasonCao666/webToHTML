import pandas as pd
import csv
import json
import urllib2
import random
import sys
import os
import re

reload(sys)
sys.setdefaultencoding("utf-8")

#remove BOM
def removeBom(file):
    BOM = b'\xef\xbb\xbf'
    existBom = lambda s: True if s==BOM else False
                
    f = open(file, 'rb')
    if existBom( f.read(3) ):
        fbody = f.read()
        with open(file, 'wb') as f:
            f.write(fbody)
    f.close
#get HTML content
def getContent(url,headers):
    random_header = random.choice(headers)
    try:
        req =urllib2.Request(url)
    except urllib2.HTTPError, err:
        print err.code
    except urllib2.URLError, err:
        print err
    req.encoding='utf-8'
    req.add_header("User-Agent", random_header)
    req.add_header("GET",url)
    try:
        content=urllib2.urlopen(req).read()
    except urllib2.HTTPError, err:
        print err.code
        return -1
    except urllib2.URLError, err:
        print err
        return -1
    return content

#get coordination
def getCoordination(city_name):
    for i in range(len(list_coordination)):
        if city_name==list_coordination[i]['city']:
            return list_coordination[i]['coordination']
    return 'empty'


my_headers = ["Mozilla/5.0 (Windows NT 6.3; Win64; x64)  (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"]


#load coordination csv file
list_coordination=[]
removeBom('/Users/mac/Documents/Dissertation/documents/coordination.csv')
with open('/Users/mac/Documents/Dissertation/documents/coordination.csv','rb') as csv_coordination:
    reader_coordination = csv.DictReader(csv_coordination,delimiter=',')
    for coordination in reader_coordination:
        if coordination['city']!='':
            coordination['coordination']=coordination['coordination'].replace(' ','')
            list_coordination.append(coordination)
    csv_coordination.close


#load menuwebsite csv file and get HTML content
list_rows=[]
index=0;
HTML_id_websites=[]
removeBom('/Users/mac/Documents/Dissertation/documents/London.csv')
with open('/Users/mac/Documents/Dissertation/documents/London.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=',')
    for row in reader:
        result_row = []
        id_website_content=[]
        if row['ID']!='':
            #result_row.append(getContent(row['Website'],my_headers))
            result_row.append(row['ID'])
            result_row.append(getCoordination(row['Town']))
            result_row.append(row['ID']+'.csv')
            
            id_website_content.append(row['ID']+'.csv')
            id_website_content.append(getContent(row['Website'],my_headers))
            
            #print len(result_dic)
            index=index+1
            list_rows.append(result_row)
            HTML_id_websites.append(id_website_content)
    csvfile.close
#print index
print len(list_rows[0])


#if file exist, delete
filename = '/Users/mac/Documents/Dissertation/documents/test_HTML_filename.csv'
if os.path.exists(filename):
    os.remove(filename)


#write file
headers = ['id','coordination','HTML_file_name']
with open(filename,'wb') as final_file:
    csvWriter = csv.writer(final_file)
    csvWriter.writerow(headers)
    for data in list_rows:
        csvWriter.writerow(data)
    final_file.close

for H_content in HTML_id_websites:
    HTML_content_filename = '/Users/mac/Documents/Dissertation/HTML/'+H_content[0]
    if os.path.exists(HTML_content_filename):
        os.remove(HTML_content_filename)

#write HTML content into seperate files
header = ['HTML_content']
for H_content in HTML_id_websites:
    HTML_content_filename = '/Users/mac/Documents/Dissertation/HTML/'+H_content[0]
    with open(HTML_content_filename,'wb') as HTML_result_file:
        csvWriter = csv.writer(HTML_result_file)
        csvWriter.writerow(header)
        csvWriter.writerow([H_content[1]])
    HTML_result_file.close






