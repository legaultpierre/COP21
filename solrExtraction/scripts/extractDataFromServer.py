#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests

from lxml import etree
base = 'http://jiminy.medialab.sciences-po.fr/solr/hyphe-cop21-1-new-schema/tvrh?q=*%3A*&fl=text&tv.tf=true&rows=10&start='
jsonObject = {}

def generateURLs(base, lastCall, step):
  urls = []
  for i in xrange(0, lastCall, step):
    # string = base + '%d'
    urls.append(base + str(i))
  return urls

def indexContent(url):
  response = requests.get(url)

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

for url in generateURLs(base, 4790, 10):
  indexContent(url)
export()
