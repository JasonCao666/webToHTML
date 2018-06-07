import csv
import re
import sys
import os
import pandas as pd
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


filted_result_list=[]
path='/Users/mac/Documents/Dissertation/HTML/'
for input_row in input_list:
    filter_result=[]
    filter_result.append(input_row[0])
    filter_result.append(input_row[1])
    
    re_head = re.compile('<\s*head[^>]*>(.*?)<\s*/\s*head\s*>', re.I|re.S|re.M)
    re_script = re.compile('<\s*script[^>]*>(.*?)<\s*/\s*script\s*>', re.I|re.S|re.M)
    re_style = re.compile('<\s*style[^>]*>(.*?)<\s*/\s*style\s*>', re.I|re.S|re.M)
    re_newline = re.compile('\n')
    re_space = re.compile('\t')
    re_six=re.compile('(?i)^((0x)?([a-f\d])+,\s)*(0x)?([a-f\d])+$')
    re_encode=re.compile(r'\\([a-zA-Z])([a-zA-Z0-9]){2}')
    re_extra_character=re.compile(r'__')
    re_HTML_tag1=re.compile(r'<')
    re_HTML_tag2=re.compile(r'/')
    re_HTML_tag3=re.compile(r'>')
    
    with open(path+input_row[2],'rb') as csv_HTML:
        HTML_reader = csv.DictReader(csv_HTML,delimiter=',')
        for HTML_content in HTML_reader:
            filter_HTML=re_head.sub('',HTML_content['HTML_content'])
            filter_HTML=re_script.sub('',filter_HTML)
            filter_HTML=re_style.sub('',filter_HTML)
            filter_HTML=re_newline.sub('',filter_HTML)
            filter_HTML=re_space.sub('',filter_HTML)
    
            filter_HTML=re_extra_character.sub('',filter_HTML)
            filter_HTML=re_HTML_tag1.sub(' ',filter_HTML)
            filter_HTML=re_HTML_tag2.sub(' ',filter_HTML)
            filter_HTML=re_HTML_tag3.sub(' ',filter_HTML)
            filter_result.append(filter_HTML)
    csv_HTML.close
    filted_result_list.append(filter_result)


print filter_result[0]
#print list_HTML
split_result=[]
word_location_map_result=[]
for i in range(len(filted_result_list)):
    split_result=filted_result_list[i][2].split()
    for j in range(len(split_result)):
        word_location_row=[]
        word_location_row.append(filted_result_list[i][0])
        word_location_row.append(filted_result_list[i][1])
        word_location_row.append(split_result[j])
        word_location_map_result.append(word_location_row)
word_location_map_result=sorted(word_location_map_result)



#if file exist, delete
output_filename = '/Users/mac/Documents/Dissertation/documents/wordLocation.csv'
if os.path.exists(output_filename):
    os.remove(output_filename)

'''for k in range(len(word_location_map_result)):
    write_rows=pd.DataFrame([word_location_map_result[k]])
    write_rows.to_csv('wordLocation.csv', mode='a', index=False,sep=',', header=None)'''

headers = ['id', 'coordination', 'word']
with open(output_filename,'wb') as output_file:
    csvWriter = csv.writer(output_file)
    csvWriter.writerow(headers)
    for data in word_location_map_result:
        csvWriter.writerow(data)
    output_file.close

