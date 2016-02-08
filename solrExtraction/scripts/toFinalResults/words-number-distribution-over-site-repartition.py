import json
import os

# Gets the data from the given folder
def loadData(file):
  with open(file) as f :
    json_data=f.read()
    return json.loads(json_data)

def drange(start, stop, step):
  r = start
  while r < stop:
    yield r
    r += step

def exportList(fileName, string):
  path = '../../finalResults/'
  s = 'Word repartition with a count of minimum 5000 occurences, by site representation proportion.\n'
  s += string
  if not os.path.exists(path):
    os.makedirs(path)
  with open(path + fileName + '.txt', 'w') as outfile:
    outfile.write(s)

def generateWordStat(maxOccur, minOccur, maxRate, minRate, step):
  repartitionIndex = []
  for k in drange(minRate, maxRate, step):
    filePath = '../../extractedData/wordIndexLinksWithWE/wordIndexLinksWithWE_%d_%d_%.6f_%.6f.json' % (maxOccur, minOccur, maxRate, k)
    repartitionIndex.append({'rate':k, 'count':len(loadData(filePath))})
  return repartitionIndex

def generateStringFromList(list):
  return '\n'.join(['%.3f\t%d' % (m['rate'], m['count']) for m in list])

def main():
  maxOccur = 200000000
  minOccur = 5000
  minRate = 0
  maxRate = 1
  step = 0.05
  wordList = generateWordStat(maxOccur, minOccur, maxRate, minRate, step)
  print wordList
  base = 'COP21-1-words-number-repartition-over-site-repartition'
  exportList(base, generateStringFromList(wordList))

if __name__=='__main__':
  main()
