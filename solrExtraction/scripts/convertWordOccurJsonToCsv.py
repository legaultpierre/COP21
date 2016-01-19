# coding: utf8

import sys
import json
import time
from os import listdir
from os.path import isfile, join


# Gets all the files at the given folderPath
def getFiles(folderPath):
  return [f for f in listdir(folderPath) if isfile(join(folderPath, f))]

# Gets the data from the given folder
def loadData(file):
  with open(file) as f :
    json_data=f.read()
    return json.loads(json_data)
    
    
def main():
  folder = '../extractedData/topWords/indexesByWE/'
  files = getFiles(folder)
  for f in files:
    f2 = f[:-4]
    f2=f2+'csv'
    export('word,occurence\n', '/'+f2)
    fileData = loadData(folder + f)
    for couple in fileData:
      mot = couple[0]
      nbOccur = couple[1]
      export(mot.encode('utf-8'), '/' + f2)
      export(',', '/' + f2)
      export(str(nbOccur), '/' + f2)
      export('\n', '/' + f2)
    
    
# Exports the result to a file
def export(string, fileName):
  with open('../extractedData/topWords/indexesByWE/csvFiles/' + fileName, 'a') as outfile:
      outfile.write(string)
      
      
if __name__=='__main__':
  main()