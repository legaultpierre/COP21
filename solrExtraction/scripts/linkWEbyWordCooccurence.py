import sys
import csv
import json
import os
from os import listdir
from os.path import isfile, join

webentities_file = 'COP21.csv'

def createWeList():
  weList = []
  # Iterate over the web entities
  with open(webentities_file) as f :
    i = 0
    for webentity in csv.DictReader(f) :
      i = i + 1
      # Get the necessary info from CSV
      id = webentity['ID']
      name = webentity['NAME']
      status = webentity['STATUS']

      if webentity['STATUS'] == 'IN':
        weList.append(id)

  return weList

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

def filterWordIndex(wordIndex, weList, maximalCount, minimalCount, rateMax, rateMin):
  newIndex = {}
  maxLinks = (len(weList)*rateMax)
  minLinks = (len(weList)*rateMin)
  for word in wordIndex:
    # Filters by the occurence count
    if ((wordIndex[word]['count'] <= maximalCount) and
        (wordIndex[word]['count'] >= minimalCount)):
      wesNumber = (len(wordIndex[word]['wes']))
      if (
          wesNumber <= maxLinks and
          wesNumber >= minLinks
        ):
        print word
        print '%f, %f, %d' % (minLinks, maxLinks, (len(wordIndex[word]['wes'])))
        newIndex[word] = wordIndex[word]
  return newIndex

def export(jsonObject, fileName):
  path = '../extractedData/wordIndexLinksWithWE/'
  if not os.path.exists(path):
    os.makedirs(path)
  with open(path + fileName + '.json', 'w') as outfile:
    json.dump(jsonObject, outfile)


def main():
  weList = createWeList()
  print weList
  folder = '../extractedData/topWords/indexesByWE/'
  files = getFiles(folder)
  index = {}
  wordIndex = {}
  maxCount = 200000000
  minCount = 5000
  maxRate = 0.5
  minRate = 0.0
  for f in files:
    we = f[:-5]
    index[we] = loadData(folder + f)
    indexWords(we, index[we], wordIndex)
  wordIndex = filterWordIndex(wordIndex, weList, maxCount, minCount, maxRate, minRate)
  fileName = 'wordIndexLinksWithWE_%d_%d_%f_%f' % (maxCount, minCount, maxRate, minRate)
  export(wordIndex, fileName)


if __name__=='__main__':
  main()
