import sys
import json
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
def export(jsonObject, fileName):
  with open('../extractedData/topWords/' + fileName, 'w') as outfile:
      json.dump(jsonObject, outfile)

def main(modeNumber):
  if (modeNumber == 0):
    mode = 'indexedByTag'
  else:
    mode = 'indexesByWE'
  folder = '../extractedData/' + mode + '/'
  files = getFiles(folder)
  for f in files:
    fileData = loadData(folder + f)
    words = fileData['joinedData']
    sortedWords = sortWords(words)
    export(sortedWords, mode + '/' + f)

if __name__=='__main__':
  arguments = sys.argv
  mode = 0
  if (len(arguments) == 2):
    if (arguments[1] > 1):
      mode = 1
  main(mode)
