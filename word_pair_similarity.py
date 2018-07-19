import csv
import spacy
import os

word_pair_list=[]
with open('/Users/mac/Documents/Dissertation/documents/wordPair_collection_result.csv','rb') as csv_word_pair:
    reader_word_pairs = csv.DictReader(csv_word_pair,delimiter=',')
    for word_pair in reader_word_pairs:
        if word_pair['word']!='':
            word_pair_list.append((word_pair['word'], word_pair['coordinations']))
    csv_word_pair.close

nlp = spacy.load('en')
output_list=[]
for i in range(len(word_pair_list)):
    compare1=nlp(u'%s' % (word_pair_list[i][0]))
    for word_pair in word_pair_list:
        compare2=nlp(u'%s' % (word_pair[0]))
        pro=round(float(compare1.similarity(compare2)),2)
        if pro>=0.8:
            output_list.append((word_pair_list[i][0],word_pair[0],pro))

#if file exist, delete
output_filename = '/Users/mac/Documents/Dissertation/documents/similarity_result.csv'
if os.path.exists(output_filename):
    os.remove(output_filename)

#write result into wordLocation.csv
headers = ['word', 'similar_word','similarity']
with open(output_filename,'wb') as output_file:
    csvWriter = csv.writer(output_file)
    csvWriter.writerow(headers)
    for data in output_list:
        csvWriter.writerow(data)
output_file.close
