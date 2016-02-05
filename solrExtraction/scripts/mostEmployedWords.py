import sys
import json
import os
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

# Returns the second argument of a list
def getCount(wordObject):
  return wordObject[1]

# Returns the a list of ['word', count] sorted by descending count
def sortWords(words):
  list = []
  for word in words:
    wordObject = []
    wordObject.append(word)
    wordObject.append(words[word])
    list.append(wordObject)
  return sorted(list, key=getCount, reverse=True)

# Exports the result to a file
def export(jsonObject, fileName,path):
  #path = '../extractedData/topWords/'
  if not os.path.exists(path):
    os.makedirs(path)
  with open(path + fileName + '.json', 'w') as outfile:
    json.dump(jsonObject, outfile)

def byWE():
  mode = 'indexesByWE'
  path='../extractedData/topWords/' + mode + '/'
  folder = '../extractedData/' + mode + '/'
  files = getFiles(folder)
  for f in files:
    fileData = loadData(folder + f)
    words = fileData['joinedData']
    fileName=f[:-5]
    sortedWords = sortWords(words)
    export(sortedWords, fileName, path)

def byTAG():
  mode = 'indexedByTag'
  folder = '../extractedData/' + mode + '/'
  files = getFiles(folder)
  for f in files:
    tag=f[:-5]
    #print tag
    path='../extractedData/topWords/'+ mode + '/' + tag + '/'
    #print path
    fileData = loadData(folder + f)
    for value in fileData:
      fileName=value
      words = fileData[value]
      sortedWords = sortWords(words)
      export(sortedWords,value,path)



def main(modeNumber):
  if (modeNumber == 0):
    byWE()
  else:
    byTAG()

if __name__=='__main__':
  arguments = sys.argv
  mode = 0
  if (len(arguments) == 2):
    if (arguments[1] >= 1):
      mode = 1
  main(mode)
