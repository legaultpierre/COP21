#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
import time

from lxml import etree

# def generateURLs(base, lastCall, step):
#   urls = []
#   for i in xrange(0, lastCall, step):
#     # string = base + '%d'
#     urls.append(base + str(i))
#   return urls


def verifyRequest(url, it, max):
  response = requests.get(url)
  if (response.status_code == 200):
    return response
  elif (it < max):
    time.sleep(2)
    return verifyRequest(url, it + 1, max)
  else :
    return -1


def indexContent(urlStart, j, jsonJoin, jsonObject, we):
  urlWithJ = urlStart + str(j)
  print urlWithJ
  response = verifyRequest(urlWithJ, 0, 20)
  if (response == -1):
    print('ERROR: ' + url)
  else :
    tree = etree.fromstring(response.content)
    # tree = etree.parse('../tvrh.xml')

    if j == 0:
      numOfPages = int(tree.xpath('/response/result')[0].get('numFound'))
      print numOfPages
    
    # print tree.xpath('/response//lst[@name="termVectors"]/lst')
    i = 0
    for page in tree.xpath('/response//lst[@name="termVectors"]/lst'):
      #jsonData = json.loads(jsonObject)
      
      pageObject = {}
    
      url = '/response//lst[@name="termVectors"]'
      namePage = page.get('name')
      url = url + '//lst[@name="' + namePage + '"]//lst[@name="text"]/lst'
      
      listOfWordElements = tree.xpath(url)
      wordsObject = {}
	  
      for wordElement in listOfWordElements:
        word = wordElement.get('name')
        
        value = int(wordElement.getchildren()[0].text)
        wordsObject[word] = value
        
        if word in jsonJoin:
          jsonJoin[word] = jsonJoin[word] + value
        else:
          jsonJoin[word] = value
      i = i + 1
      
      pageObject['words'] = wordsObject
      jsonObject[namePage] = pageObject

    if j == 0:
      for k in xrange(10, (numOfPages//10) * 10, 10):
        print k
        indexContent(urlStart, k, jsonJoin, jsonObject, we)
