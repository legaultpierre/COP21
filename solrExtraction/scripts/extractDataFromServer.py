#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests

from lxml import etree
base = 'http://jiminy.medialab.sciences-po.fr/solr/hyphe-cop21-1-new-schema/tvrh?q=*%3A*&fl=text&tv.tf=true&rows=10&start='
# q=web_entity_id:
jsonObject = {}

def generateURLs(base, lastCall, step):
  urls = []
  for i in xrange(0, lastCall, step):
    # string = base + '%d'
    urls.append(base + str(i))
  return urls

def verifyRequest(url, it, max):
  response = requests.get(url)
  if (response.status_code == 200):
    return response
  elif (it < max):
    time.sleep(2)
    return verifyRequest(url, it + 1, max)
  else :
    return -1

def indexContent(url):
  response = verifyRequest(url, 0, 20)
  if (response == -1):
    print('ERROR: ' + url)
  else :
    tree = etree.fromstring(response.content)
    # tree = etree.parse('../tvrh.xml')


    # print tree.xpath('/response//lst[@name="termVectors"]/lst')
    index = 0
    for page in tree.xpath('/response//lst[@name="termVectors"]/lst'):
      pageObject = {}
      url = '/response//lst[@name="termVectors"]'
      namePage = page.get('name')
      url = url + '//lst[@name="' + namePage + '"]//lst[@name="text"]/lst'

      listOfWordElements = tree.xpath(url)
      wordsObject = {}
      for wordElement in listOfWordElements:
        word =  wordElement.get('name')
        value = int(wordElement.getchildren()[0].text)
        wordsObject[word] = value
      index = index + 1
      pageObject['words'] = wordsObject
      jsonObject[namePage] = pageObject

def export():
  with open('../extractedData/extractedWords.json', 'w') as outfile:
      json.dump(jsonObject, outfile)

i = 0
for url in generateURLs(base, 4790, 10):
  print i
  indexContent(url)
  i = i + 1
export()
