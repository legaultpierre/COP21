#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import extractDataFromServer
import os
import time

webentities_file = 'COP21_tags.csv'

def try_utf8(data):
    "Returns a Unicode object on success, or None on failure"
    try:
       return data.encode('utf-8')
    except UnicodeDecodeError:
       return None

def getTagsOfWE():
  tags = ['ACTORS_TYPE','AREA','COUNTRY','ANTHROPOGENIC_CLIMATE_CHANGE','MITIGATION_ADAPTATION','INDUSTRIAL_DELEGATION','THEMATIC_DELEGATION','COLLECTION']
  with open(webentities_file) as f :
    countError=0
    for tag in tags:
      # On cree le JSON
      values = {}
      count=0
      f.seek(0)
      for we in csv.DictReader(f) :
        print count
        count=count+1
        uvalTag = try_utf8(we[tag])
        if uvalTag is None:
          countError = countError+1
          print 'Error'
        else :
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
    print countError

def export(jsonObject, tag):
  folder = '../extractedData/indexedByTag/'
  with open(folder +'/'+tag+ '.json', 'w') as outfile:
    json.dump(jsonObject, outfile)

def main():
  getTagsOfWE()

main()
