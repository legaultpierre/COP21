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

def indexWords(we, newData, wordIndex):
  for element in newData:
    word = element[0]
    count = element[1]
    if word not in wordIndex:
      wordIndex[word] = {}
      wordIndex[word]['count'] = count
      wordIndex[word]['wes'] = {}
      wordIndex[word]['wes'][we] = count
    else :
      wordIndex[word]['count'] += count
      wordIndex[word]['wes'][we] = count

def filterWordIndex(wordIndex):
  newIndex = {}
  for word in wordIndex:
    if ((wordIndex[word]['count'] > 99) & (len(wordIndex[word]['wes']) > 1)):
      newIndex[word] = wordIndex[word]
  return newIndex

def export(jsonObject, fileName):
  with open('../extractedData/' + fileName + '.json', 'w') as outfile:
    json.dump(jsonObject, outfile)


def main():
  folder = '../extractedData/topWords/indexesByWE/'
  files = getFiles(folder)
  index = {}
  wordIndex = {}
  for f in files:
    we = f[:-5]
    index[we] = loadData(folder + f)
    indexWords(we, index[we], wordIndex)
  wordIndex = filterWordIndex(wordIndex)
  export(wordIndex, 'wordIndexLinksWithWE')


if __name__=='__main__':
  main()
