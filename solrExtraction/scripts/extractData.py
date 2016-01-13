import csv
import json
import extractDataFromServer

webentities_file = 'COP21.csv'

def createWeIndex():
  weIndex = {}
  # Iterate over the web entities
  with open(webentities_file) as f :
    i = 0
    for webentity in csv.DictReader(f) :
      i = i + 1
      # Get the necessary info from CSV
      id = webentity['ID']
      name = webentity['NAME']
      status = webentity['STATUS']
      lrus = convertSpaceSeparatedValueToArray(webentity['PREFIXES AS LRU'])

      if webentity['STATUS'] == 'IN':
        weIndex[id] = {}
        weIndex[id]['lrus'] = lrus
        weIndex[id]['name'] = name
        weIndex[id]['data'] = {}

  return weIndex

def convertSpaceSeparatedValueToArray(string):
  if string == '':
    return []
  else :
    return string.split(' ')

def export(jsonObject, fileName):
  with open('../extractedData/indexesByWE/' + fileName + '.json', 'w') as outfile:
      json.dump(jsonObject, outfile)


def generateURLByWE(weIndex):
  base = 'http://jiminy.medialab.sciences-po.fr/solr/hyphe-cop21-1-new-schema/tvrh?q=web_entity_id:'
  end = '&fl=text&tv.tf=true&rows=10&start=0'
  for we in weIndex:
    url = base + we + end
    print url
    extractDataFromServer.indexContent(url, weIndex[we]['data'])
    print weIndex[we]['data']
    export(weIndex[we], we)

def main():
  print 'hey'
  index = createWeIndex()
  print index
  generateURLByWE(index)
  export(index)

main()
