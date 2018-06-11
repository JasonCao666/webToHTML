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
    
    re_all_tag1 = re.compile(r'<\s*[^>]*\s*>', re.I|re.S|re.M)
    re_all_tag2 = re.compile(r'<\s*/[^>]*\s*>', re.I|re.S|re.M)
    re_all_tag3 = re.compile(r'{\s*[^}]*\s*}', re.I|re.S|re.M)
    re_all_tag4 = re.compile(r'\"[^\"]*\"', re.I|re.S|re.M)
    
    re_head = re.compile('<\s*head[^>]*>(.*?)<\s*/\s*head\s*>', re.I|re.S|re.M)
    re_script = re.compile('<\s*script[^>]*>(.*?)<\s*/\s*script\s*>', re.I|re.S|re.M)
    re_style = re.compile('<\s*style[^>]*>(.*?)<\s*/\s*style\s*>', re.I|re.S|re.M)
    re_a = re.compile('<\s*a[^>]*>(.*?)<\s*/\s*a\s*>', re.I|re.S|re.M)
    re_img = re.compile('<\s*img[^>]*/>', re.I|re.S|re.M)
    re_HTML_li1=re.compile(r'<li[^>]*>')
    re_HTML_li2=re.compile(r'</li>')
    re_HTML_p1=re.compile(r'<p[^>]*>')
    re_HTML_p2=re.compile(r'</p>')
    re_HTML_div1=re.compile(r'<div[^>]*>')
    re_HTML_div2=re.compile(r'</div>')
    re_HTML_strong1=re.compile(r'<strong[^>]*>')
    re_HTML_strong2=re.compile(r'</strong>')
    re_HTML_ul1=re.compile(r'<ul[^>]*>')
    re_HTML_ul2=re.compile(r'</ul>')
    re_HTML_h1=re.compile(r'<h[0-9][^>]*>')
    re_HTML_h2=re.compile(r'</h[0-9]>')
    re_HTML_tr1=re.compile(r'<tr[^>]*>')
    re_HTML_tr2=re.compile(r'</tr>')
    re_HTML_td1=re.compile(r'<td[^>]*>')
    re_HTML_td2=re.compile(r'</td>')
    re_HTML_dt1=re.compile(r'<dt[^>]*>')
    re_HTML_dt2=re.compile(r'</dt>')
    re_HTML_dd1=re.compile(r'<dd[^>]*>')
    re_HTML_dd2=re.compile(r'</dd>')
    re_HTML_br1=re.compile(r'<br[^>]*>')
    re_HTML_br2=re.compile(r'</br>')
    
    re_HTML_ids=re.compile(r'id="[^"]')
    re_newline = re.compile('\n')
    re_space = re.compile('\t')
    re_six=re.compile('(?i)^((0x)?([a-f\d])+,\s)*(0x)?([a-f\d])+$')
    re_encode=re.compile(r'\\([a-zA-Z])([a-zA-Z0-9]){2}')
    re_extra_character=re.compile(r'__')
    re_HTML_tag1=re.compile(r'<')
    re_HTML_tag2=re.compile(r'/')
    re_HTML_tag3=re.compile(r'>')
    re_HTML_tag4=re.compile(r'="(.*?)"')
    re_HTML_tag5=re.compile(r'class')
    re_HTML_tag6=re.compile(r'style')
    re_HTML_tag7=re.compile(r'!--')
    re_HTML_tag8=re.compile(r'span')
    re_HTML_tag9=re.compile(r'html')
    re_HTML_tag10=re.compile(r'--')
    re_HTML_tag11=re.compile(r'\|')
    re_HTML_tag12=re.compile(r'-')
    re_HTML_tag13=re.compile(r'&nbsp;')
    re_HTML_tag14=re.compile(r'\.')
    re_HTML_tag15=re.compile(r':')
    re_HTML_tag16=re.compile(r'&')
    re_HTML_tag17=re.compile(r'\xc2')
    re_HTML_tag18=re.compile(r',')
    re_HTML_tag19=re.compile(r';')
    re_HTML_tag20=re.compile(r'!DOCTYPE')
    
    re_HTML_tag21=re.compile(r'\[')
    re_HTML_tag22=re.compile(r'\]')
    re_HTML_tag23=re.compile(r'{')
    re_HTML_tag24=re.compile(r'}')
    re_HTML_tag25=re.compile(r'\+')
    re_HTML_tag26=re.compile(r'\(')
    re_HTML_tag27=re.compile(r'\)')
    re_HTML_tag28=re.compile(r'\\')
    re_HTML_tag29=re.compile(r'=')
    re_HTML_tag30=re.compile(r'\*')
    re_HTML_numbers=re.compile(r'[0-9]')
    re_HTML_items=re.compile(r'item[^\s]+\s')
    
    with open(path+input_row[2],'rb') as csv_HTML:
        HTML_reader = csv.DictReader(csv_HTML,delimiter=',')
        for HTML_content in HTML_reader:
            filter_HTML=re_all_tag1.sub(' ',HTML_content['HTML_content'])
            filter_HTML=re_all_tag2.sub(' ',filter_HTML)
            filter_HTML=re_all_tag3.sub(' ',filter_HTML)
            filter_HTML=re_all_tag4.sub(' ',filter_HTML)
            '''filter_HTML=re_head.sub('',filter_HTML)
            filter_HTML=re_script.sub('',filter_HTML)
            filter_HTML=re_style.sub('',filter_HTML)
            filter_HTML=re_a.sub(' ',filter_HTML)
            filter_HTML=re_img.sub(' ',filter_HTML)
            filter_HTML=re_HTML_li1.sub(' ',filter_HTML)
            filter_HTML=re_HTML_li2.sub(' ',filter_HTML)
            
            filter_HTML=re_HTML_p1.sub(' ',filter_HTML)
            filter_HTML=re_HTML_p2.sub(' ',filter_HTML)
            filter_HTML=re_HTML_div1.sub(' ',filter_HTML)
            filter_HTML=re_HTML_div2.sub(' ',filter_HTML)
            filter_HTML=re_HTML_strong1.sub(' ',filter_HTML)
            filter_HTML=re_HTML_strong2.sub(' ',filter_HTML)
            filter_HTML=re_HTML_ul1.sub(' ',filter_HTML)
            filter_HTML=re_HTML_ul2.sub(' ',filter_HTML)
            filter_HTML=re_HTML_h1.sub(' ',filter_HTML)
            filter_HTML=re_HTML_h2.sub(' ',filter_HTML)
            filter_HTML=re_HTML_tr1.sub(' ',filter_HTML)
            filter_HTML=re_HTML_tr2.sub(' ',filter_HTML)
            filter_HTML=re_HTML_td1.sub(' ',filter_HTML)
            filter_HTML=re_HTML_td2.sub(' ',filter_HTML)
            filter_HTML=re_HTML_dt1.sub(' ',filter_HTML)
            filter_HTML=re_HTML_dt2.sub(' ',filter_HTML)
            filter_HTML=re_HTML_dd1.sub(' ',filter_HTML)
            filter_HTML=re_HTML_dd2.sub(' ',filter_HTML)
            filter_HTML=re_HTML_br1.sub(' ',filter_HTML)
            filter_HTML=re_HTML_br2.sub(' ',filter_HTML)'''
           
            filter_HTML=re_HTML_numbers.sub(' ',filter_HTML)
            filter_HTML=re_HTML_ids.sub(' ',filter_HTML)
            
            filter_HTML=re_extra_character.sub('',filter_HTML)
            filter_HTML=re_HTML_tag1.sub(' ',filter_HTML)
            filter_HTML=re_HTML_tag2.sub('',filter_HTML)
            filter_HTML=re_HTML_tag3.sub(' ',filter_HTML)
            filter_HTML=re_HTML_tag4.sub(' ',filter_HTML)
            filter_HTML=re_HTML_tag5.sub('',filter_HTML)
            filter_HTML=re_HTML_tag6.sub('',filter_HTML)
            filter_HTML=re_HTML_tag7.sub('',filter_HTML)
            filter_HTML=re_HTML_tag8.sub('',filter_HTML)
            filter_HTML=re_HTML_tag9.sub('',filter_HTML)
            filter_HTML=re_HTML_tag10.sub('',filter_HTML)
            filter_HTML=re_HTML_tag11.sub('',filter_HTML)
            filter_HTML=re_HTML_tag12.sub('',filter_HTML)
            filter_HTML=re_HTML_tag13.sub('',filter_HTML)
            filter_HTML=re_HTML_tag14.sub('',filter_HTML)
            filter_HTML=re_HTML_tag15.sub('',filter_HTML)
            filter_HTML=re_HTML_tag16.sub('',filter_HTML)
            filter_HTML=re_HTML_tag17.sub('',filter_HTML)
            filter_HTML=re_HTML_tag18.sub('',filter_HTML)
            filter_HTML=re_HTML_tag19.sub('',filter_HTML)
            filter_HTML=re_HTML_tag20.sub('',filter_HTML)
            filter_HTML=re_HTML_tag21.sub('',filter_HTML)
            filter_HTML=re_HTML_tag22.sub('',filter_HTML)
            filter_HTML=re_HTML_tag23.sub('',filter_HTML)
            filter_HTML=re_HTML_tag24.sub('',filter_HTML)
            filter_HTML=re_HTML_tag25.sub('',filter_HTML)
            filter_HTML=re_HTML_tag26.sub('',filter_HTML)
            filter_HTML=re_HTML_tag27.sub('',filter_HTML)
            filter_HTML=re_HTML_tag28.sub('',filter_HTML)
            filter_HTML=re_HTML_tag29.sub('',filter_HTML)
            filter_HTML=re_HTML_tag30.sub('',filter_HTML)
            filter_HTML=re_HTML_items.sub(' ',filter_HTML)
            filter_HTML=re_newline.sub('',filter_HTML)
            filter_HTML=re_space.sub('',filter_HTML)
            filter_result.append(filter_HTML)
    csv_HTML.close
    filted_result_list.append(filter_result)

print len(filted_result_list)

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
print len(word_location_map_result)

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

