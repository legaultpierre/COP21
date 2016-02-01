import sys
import csv
import json
import os
from os import listdir
from os.path import isfile, join

webentities_file = 'COP21_tags.csv'

def createTagIndex():
  tagIndex = {}
  # Iterate over the web entities
  with open(webentities_file) as f :
    i = 0
    #tags=['ACTORS_TYPE']
    tags=['ACTORS_TYPE','AREA','COUNTRY','ANTHROPOGENIC_CLIMATE_CHANGE','MITIGATION_ADAPTATION','INDUSTRIAL_DELEGATION','THEMATIC_DELEGATION','COLLECTION']#,'ABSTRACT_DRAFT','ABSTRACT','COMMENT']
    for tag in tags :
      tagIndex[tag]={}
      tagIndex[tag]['values']=[]
    for webentity in csv.DictReader(f) :
      i = i + 1
      # Get the necessary info from CSV
      status = webentity['STATUS']
      if webentity['STATUS'] == 'IN':
        for tag in tags:
          if webentity[tag] not in tagIndex[tag]['values']:
            tagIndex[tag]['values'].append(webentity[tag])
            #print tagIndex[tag]['values']
  return tagIndex



# Gets all the files at the given folderPath
def getFiles(folderPath):
  return [f for f in listdir(folderPath) if isfile(join(folderPath, f))]

# Gets the data from the given folder
def loadData(file):
  with open(file) as f :
    json_data=f.read()
    return json.loads(json_data)

def indexWords(newData, wordIndex):
  for value in newData :
    for element in newData[value]:
      word = element
      count = newData[value][word]
      #print count
      if word not in wordIndex:
        wordIndex[word] = {}
        wordIndex[word]['count'] = count
        wordIndex[word]['values']={}
        wordIndex[word]['values'][value] = count
      else :
        #print count
        wordIndex[word]['count'] += count
        wordIndex[word]['values'][value] = count

def numberTagValues(tagIndex,tag):
  return len(tagIndex[tag]['values'])

def filterWordIndex(tag,wordIndex, tagIndex, maximalCount, minimalCount, rateMax, rateMin):
  newIndex = {}
  numbertagvalues = numberTagValues(tagIndex,tag)
  print numbertagvalues
  maxLinks = (numbertagvalues*rateMax)
  minLinks = (numbertagvalues*rateMin)
  for word in wordIndex:
    # Filters by the occurence count
    if ((wordIndex[word]['count'] <= maximalCount) and
        (wordIndex[word]['count'] >= minimalCount)):
      tagsNumber = (len(wordIndex[word]['values']))
      #print (len(wordIndex[word]['values']))
      if (
          tagsNumber <= maxLinks and
          tagsNumber >= minLinks
        ):
        #print word
        #print '%f, %f, %d' % (minLinks, maxLinks, numberTagValuesWord(wordIndex, word))
        newIndex[word] = wordIndex[word]
  return newIndex

def export(jsonObject, fileName,tag):
  path = '../extractedData/wordIndexLinksWithTAG/'+tag+'/'
  if not os.path.exists(path):
    os.makedirs(path)
  with open(path + fileName + '.json', 'w') as outfile:
    json.dump(jsonObject, outfile)


def main():
  #weList = createWeList()
  #print weList
  tagIndex=createTagIndex()
  #print tagIndex
  folder = '../extractedData/indexedByTag/'
  files = getFiles(folder)
  index = {}
  maxCount = 200000000
  minCount = 500
  maxRate = 1
  minRate = 0.5
  fileName = 'wordIndexLinksWithTAG_%d_%d_%f_%f' % (maxCount, minCount, maxRate, minRate)
  for f in files:
    wordIndex = {}
    tag = f[:-5]
    print tag
    index[tag] = loadData(folder + f)
    indexWords(index[tag], wordIndex)
    wordIndex2 = filterWordIndex(tag,wordIndex, tagIndex, maxCount, minCount, maxRate, minRate)
    export(wordIndex2, fileName,tag)


if __name__=='__main__':
  main()
