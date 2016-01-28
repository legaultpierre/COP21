#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import extractDataFromServer
import os
import time

webentities_file = 'COP21_tags.csv'

def getTagsOfWE():
  tags = ['ACTORS_TYPE','AREA','COUNTRY','ANTHROPOGENIC_CLIMATE_CHANGE','MITIGATION_ADAPTATION','INDUSTRIAL_DELEGATION','THEMATIC_DELEGATION','COLLECTION']
  with open(webentities_file) as f :
    for tag in tags:
      # On cree le JSON
      values = {}
      count=0
      for we in csv.DictReader(f) :
        count = count + 1
        print count
        valueTag = we[tag].encode('utf-8')
        if valueTag not in values:
          values[valueTag]={}
        id = we['ID']
        with open('../extractedData/indexesByWE/' + id + '.json', 'r') as weJson:
          jsonData = json.load(weJson)
          for word in jsonData['joinedData']:
            formatOk = True
            try:
              word.encode('utf-8')
            except UnicodeEncodeError:
              formatOk = False
            if formatOk:
              if word not in values[valueTag] :
                # print jsonData['joinedData'][word]
                # print valueTag
                values[valueTag][word] = jsonData['joinedData'][word]
              else :
                values[valueTag][word] = values[valueTag][word] + jsonData['joinedData'][word]
              # if word == 'liked':
                # print word
                # time.sleep(1)
            else:
              print 'Error'
        # print values
        export(values, tag)
      print 'tag-----------------'
      print tag

def export(jsonObject, tag):
  folder = '../extractedData/indexedByTag/'
  with open(folder +'/'+tag+ '.json', 'w') as outfile:
    json.dump(jsonObject, outfile)
        
# def createTagIndex():
  # tagIndex = {}
  # Iterate over the web entities
  # with open(webentities_file) as f :
    # i = 0
    # tags=['ACTORS_TYPE','AREA','COUNTRY','ANTHROPOGENIC_CLIMATE_CHANGE','MITIGATION_ADAPTATION','INDUSTRIAL_DELEGATION','THEMATIC_DELEGATION','COLLECTION']#,'ABSTRACT_DRAFT','ABSTRACT','COMMENT']
    # for tag in tags :
      # print tag
      # tagIndex[tag]={}
      # tagIndex[tag]['values']=[]
      # tagIndex[tag]['data']={}
      # tagIndex[tag]['joinedData'] = {}
    # for webentity in csv.DictReader(f) :
      # i = i + 1
      # Get the necessary info from CSV
      # status = webentity['STATUS']
      # if webentity['STATUS'] == 'IN':
        # for tag in tags:
          # if webentity[tag] not in tagIndex[tag]['values']:
            # tagIndex[tag]['values'].append(webentity[tag])
            # print tagIndex[tag]['values']
  # return tagIndex



# def generateURLByTag(tagIndex, startWE):
  # if startWE is None:
    # found = True
  # else :
    # found = False
  
  # step = 50
  # base = 'http://jiminy.medialab.sciences-po.fr/solr/hyphe-cop21-1-new-schema/tvrh?q='
  # end = '&fl=text&tv.tf=true&rows=%d&start=' % step
  # for tag in tagIndex:
    # for v in tagIndex[tag]['values']:
      # url = base + tag + '=' + v + end
      # print url
      # tagIndex[tag]['data'][v]={}
      # extractDataFromServer.indexContent(url, 0, tagIndex[tag]['joinedData'], tagIndex[tag]['data'][v], 10)
      # export(tagIndex[tag], tag, v)
      # print tagIndex[tag]['data']

def main():
  getTagsOfWE()

main()
