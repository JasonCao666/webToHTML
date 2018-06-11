import sys
import string
import csv
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

def wordExist(input_word):
    if input_word in word_and_location.keys():
        return True
    else:
        return False

def dicHasValue(word, cor_value):
    splitword=word.split()
    for v in splitword:
        if v==cor_value:
            return True
    return False

def createDictCSV(fileName="", dataDict={}):
    with open(fileName, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)
        for k,v in dataDict.iteritems():
            csvWriter.writerow([k,v])
        csvFile.close()

index=0
word_locations=[]
current_id=None
word_and_location={}
removeBom('/Users/mac/Documents/Dissertation/documents/wordLocation.csv')
with open('/Users/mac/Documents/Dissertation/documents/wordLocation.csv','rb') as csv_HTML:
    reader_file = csv.DictReader(csv_HTML,delimiter=',')
    for file_row in reader_file:
        if current_id == None:
            current_id = file_row['id']
            word_and_location={}
            word_and_location[file_row['word']]=str(file_row['coordination'])+' '
        elif current_id != None and file_row['id']==current_id:
            if wordExist(file_row['word']):
                if dicHasValue(word_and_location[file_row['word']], file_row['coordination']):
                    continue
                else:
                    word_and_location[file_row['word']]=str(word_and_location[file_row['word']])+str(file_row['coordination'])+' '
            else:
                word_and_location[file_row['word']]=str(file_row['coordination'])+' '
        elif current_id != None and file_row['id']!=current_id:
            current_id=file_row['id']
            if wordExist(file_row['word']):
                word_and_location[file_row['word']]=str(word_and_location[file_row['word']])+str(file_row['coordination'])+' '
            #print word_and_location[file_row['word']]
            else:
                word_and_location[file_row['word']]=str(file_row['coordination'])+' '
        
        '''else:
            current_word = file_row['word']
            word_locations.append(word_and_location)
            word_and_location={}
            word_and_location['word']=file_row['word']
            word_and_location['location'] = file_row['coordination']+' '''

print word_and_location
output_file_name='/Users/mac/Documents/Dissertation/documents/collection_result.csv'
createDictCSV(output_file_name, word_and_location)

