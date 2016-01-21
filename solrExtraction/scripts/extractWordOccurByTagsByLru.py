import csv
import json
import extractDataFromServer

webentities_file = 'COP21_tags.csv'

def createTagIndex():
  tagIndex = {}
  # Iterate over the web entities
  with open(webentities_file) as f :
    i = 0
    tags=['ACTORS_TYPE','COUNTRY','AREA','ANTHROPOGENIC_CLIMATE_CHANGE','MITIGATION_ADAPTATION','INDUSTRIAL_DELEGATION','THEMATIC_DELEGATION','COLLECTION']#,'ABSTRACT_DRAFT','ABSTRACT','COMMENT']
    for tag in tags :
      print tag
      tagIndex[tag]={}
      tagIndex[tag]['values']=[]
      tagIndex[tag]['data']={}
      tagIndex[tag]['joinedData'] = {}
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

def export(jsonObject, fileName):
  with open('../extractedData/indexedByTag/' + fileName + '.json', 'w') as outfile:
      json.dump(jsonObject, outfile)

def generateURLByTag(tagIndex):
  base = 'http://jiminy.medialab.sciences-po.fr/solr/hyphe-cop21-1-new-schema/tvrh?q='
  end = '&fl=text&tv.tf=true&rows=200&start='
  for tag in tagIndex:
    for v in tagIndex[tag]['values']:
      url = base + tag + '=' + v + end
      #print url
      tagIndex[tag]['data'][v]={}
      extractDataFromServer.indexContent(url, 0, tagIndex[tag]['joinedData'], tagIndex[tag]['data'][v])
      #print tagIndex[tag]['data']
    export(tagIndex[tag], tag)

def main():
  print 'hey'
  index = createTagIndex()
  # print index
  generateURLByTag(index)
  export(index,TOUT)

main()
