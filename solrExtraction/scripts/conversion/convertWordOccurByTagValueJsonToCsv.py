# coding: utf8

import sys
import json
import time
import os
from os import listdir
from os.path import isfile, join


# Gets all the files at the given folderPath
def getFiles(folderPath):
  return [f for f in listdir(folderPath) if isfile(join(folderPath, f))]

def getDir(folderPath):
  return [f[0] for f in os.walk(folderPath)]
  
# Gets the data from the given folder
def loadData(file):
  with open(file) as f :
    json_data=f.read()
    data = json.loads(json_data)
    return data["joinedData"]
    
    
def main():
  folder = '../../extractedData/indexedByTag/'
  directories = getDir(folder)
  for d in directories:
    dir = d.split('/')
    files = getFiles(d)
    for f in files:
      f2 = f[:-4]
      f2=f2+'csv'
      export('word,occurence\n', f2, dir[3])
      fileData = loadData(folder + dir[3]+ '/' + f)
      
      for couple in fileData:
        mot = couple[0]
        nbOccur = couple.get(mot)
      print '***********************'
      print mot
      print nbOccur
      print '***********************'
        export(("%s,%d\n" % (mot, nbOccur)).encode('utf-8'), f2, dir[3])
        # export("\n".join(["%s,%d\n" % (couple[0], couple[1])] for couple in fileData]), f2)
        
        # nbOccur = couple[1]
        # export(mot.encode('utf-8'), '/' + f2)
        # export(',', '/' + f2)
        # export(str(nbOccur), '/' + f2)
        # export('\n', '/' + f2)
      
    
# Exports the result to a file
def export(string, fileName, dir):
  folder = '../../extractedData/topWords/indexedByTag/csvFiles/'
  if not os.path.exists(folder +dir):
    os.makedirs(folder +dir)
  with open(folder +dir+'/'+ fileName, 'w') as outfile:
      outfile.write(string)
      
      
if __name__=='__main__':
  main()
