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

def filterWordIndex(wordIndex, maximalCount, minimalCount, rateMax, rateMin):
  newIndex = {}
  for word in wordIndex:
    # Filters by the occurence count
    if ((wordIndex[word]['count'] < maximalCount) and
        (wordIndex[word]['count'] > minimalCount) and
        (len(wordIndex[word]['wes']) > 1 and
        (len(wordIndex[word]['wes']) <= (len(wordIndex)*rateMax)) and
        (len(wordIndex[word]['wes']) >= (len(wordIndex)*rateMin))):
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
  wordIndex = filterWordIndex(wordIndex, 600000, 5000, 1, 0.8)
  export(wordIndex, 'wordIndexLinksWithWE')


if __name__=='__main__':
  main()
