import csv
import spacy
import os

word_pair_list=[]
with open('/Users/mac/Documents/Dissertation/documents/wordPairLocation.csv','rb') as csv_word_pair:
    reader_word_pairs = csv.DictReader(csv_word_pair,delimiter=',')
    for word_pair in reader_word_pairs:
        if word_pair['word']!='':
            word_pair_list.append([word_pair['id'],word_pair['word'], word_pair['coordination']])
    csv_word_pair.close

nlp = spacy.load('en')

for i in range(len(word_pair_list)):
    new_word=''
    filter_doc = nlp(u'%s' % (word_pair_list[i][1]))
    for word in filter_doc:
        if word.pos_ =='NOUN':
            new_word=str(new_word)+str(word)+' '
    new_word=new_word.rstrip()
    new_word=new_word.lstrip()
    word_pair_list[i][1]=new_word


#if file exist, delete
output_filename = '/Users/mac/Documents/Dissertation/documents/noun_phase_filtered_result.csv'
if os.path.exists(output_filename):
    os.remove(output_filename)

#write result into wordLocation.csv
headers = ['id','word', 'coordinations']
with open(output_filename,'wb') as output_file:
    csvWriter = csv.writer(output_file)
    csvWriter.writerow(headers)
    for data in word_pair_list:
        if data[1]!='':
            csvWriter.writerow(data)
output_file.close



