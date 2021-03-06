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
            if k!='':
                csvWriter.writerow([k,v])
        csvFile.close()

index=0
word_locations=[]
current_id=None
word_and_location={}
#input_file='/Users/mac/Documents/Dissertation/documents/wordLocation.csv'
input_file='/Users/mac/Documents/Dissertation/testDocument/wordLocation.csv'
removeBom(input_file)
with open(input_file,'rb') as csv_HTML:
    reader_file = csv.DictReader(csv_HTML,delimiter=',')
    for file_row in reader_file:
        if current_id == None:
            current_id = file_row['id']
            word_and_location={}
            word_and_location[file_row['word']]=str(file_row['coordination'])+' '
        elif current_id != None and file_row['id']==current_id:
            if wordExist(file_row['word']):
                if dicHasValue(word_and_location[file_row['word']], str(file_row['coordination'])):
                    word_and_location[file_row['word']]=str(word_and_location[file_row['word']])+str(file_row['coordination'])+' '
                #print file_row['word']+' '+word_and_location[file_row['word']]
                continue
            else:
                word_and_location[file_row['word']]=str(file_row['coordination'])+' '
        elif current_id != None and file_row['id']!=current_id:
            #print 'currentId: '+ current_id + 'fileId: '+  file_row['id']
            current_id=file_row['id']
            if wordExist(file_row['word']):
                word_and_location[file_row['word']]=str(word_and_location[file_row['word']])+str(file_row['coordination'])+' '
            #print file_row['word']
            else:
                word_and_location[file_row['word']]=str(file_row['coordination'])+' '

#print word_and_location
#output_file_name='/Users/mac/Documents/Dissertation/documents/collection_result.csv'
output_file_name='/Users/mac/Documents/Dissertation/testDocument/collection_result.csv'
print word_and_location
createDictCSV(output_file_name, word_and_location)

