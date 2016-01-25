# coding: utf8
import sys, os
import json
import csv

# Gets the data from the given folder
def loadData(file):
  with open(file) as f :
    json_data=f.read()
    return json.loads(json_data)

def writeNodes(csvFileName, nodeList, outfile):
  with open(csvFileName) as f:
    outfile.write('nodedef>name VARCHAR,label VARCHAR\n')
    for webentity in csv.DictReader(f) :
      # Get the necessary info from CSV
      id = webentity['ID'].decode('utf-8')
      if (id in nodeList):
        name = webentity['NAME'].decode('utf-8')
        outfile.write(("%s,\"%s\"\n" % (id, name)).encode('utf-8'))

def writeEdges(edgesList, outfile):
  outfile.write('edgedef>node1 VARCHAR,node2 VARCHAR, label VARCHAR, weight DOUBLE\n')
  for edge in edgesList:
    outfile.write(edge)

def deleteFileIfExists(fileName):
  try:
    os.remove(fileName)
  except OSError:
      pass

def main():
  fileName = 'wordIndexLinksWithWE'
  f = '../../extractedData/' + fileName + '.json'
  outputFile = '../../extractedData/gdfFiles/' + fileName + '.gdf'
  nodeList = []
  edgesList = []
  deleteFileIfExists(outputFile)
  with open(outputFile, 'a') as outfile:
    fileData = loadData(f)
    for word in fileData:
      dataWord = fileData[word]
      wes =  dataWord['wes'].keys()
      for i in xrange(0, len(wes)):
        wei = wes[i]
        if (wei not in nodeList):
          nodeList.append(wei)
        for j in xrange(i+1, len(wes)):
          wej = wes[j]
          weight = dataWord['wes'][wei] + dataWord['wes'][wej]
          edgesList.append(("%s,%s,\"%s\",%d\n" % (wei, wej, word, weight)).encode('utf-8'))
    writeNodes('../COP21.csv', nodeList, outfile)
    writeEdges(edgesList, outfile)

if __name__=='__main__':
  main()
