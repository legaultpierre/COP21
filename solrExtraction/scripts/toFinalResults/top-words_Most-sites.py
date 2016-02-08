import json
import os

# Gets the data from the given folder
def loadData(file):
  with open(file) as f :
    json_data=f.read()
    return json.loads(json_data)

def getCount(item):
  return item['count']

def getNbWE(item):
  return item['wes']

def generateWordList():
  filePath = '../../extractedData/wordIndexLinksWithWE/wordIndexLinksWithWE_200000000_5000_1.000000_0.750000.json'
  data = loadData(filePath)
  wordList = []
  for word in data:
    wordData = data[word]
    wordObject = {}
    wordObject['word'] = word
    wordObject['count'] = wordData['count']
    wordObject['wes'] = len(wordData['wes'])
    wordList.append(wordObject)
  return wordList

def generateTopByCount(wordList):
  return sorted(wordList, key=getCount, reverse=True)

def generateTopByNbWE(wordList):
  return sorted(wordList, key=getNbWE, reverse=True)

def generateStringFromList(list, field):
  return '\n'.join(['%s\t%d' % (m['word'], m[field]) for m in list])

def exportList(fileName, string):
  path = '../../finalResults/'
  s = 'Results containing words in at least 75% of the sites and a count of minimum 5000 occurences.\n'
  s += string
  if not os.path.exists(path):
    os.makedirs(path)
  with open(path + fileName + '.txt', 'w') as outfile:
    outfile.write(s)

def main():
  wordList = generateWordList()
  print wordList
  base = 'COP21-1-top-words-most-sites-by-'
  exportList(base + 'count', generateStringFromList(generateTopByCount(wordList), 'count'))
  exportList(base + 'web-entites-links', generateStringFromList(generateTopByNbWE(wordList), 'wes'))

if __name__=='__main__':
  main()
