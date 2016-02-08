import sys
import csv
import json
import os
import re
from os import listdir
from os.path import isfile, join

webentitiesFile = '../COP21_tags.csv'
graphBaseFile = '../WE_Graph_Base.gexf'
graphExportFolder = '../../finalResults/graphFiles/'
tags=['ACTORS_TYPE','AREA','COUNTRY','ANTHROPOGENIC_CLIMATE_CHANGE','MITIGATION_ADAPTATION','INDUSTRIAL_DELEGATION','THEMATIC_DELEGATION','COLLECTION']#,'ABSTRACT_DRAFT','ABSTRACT','COMMENT']

def readGexf(): 
  file = open(graphBaseFile, "r")
  lines = file.readlines();
  return lines

def createTagIndex():
  tagIndex = {}
  # Iterate over the web entities
  with open(webentitiesFile) as f :
    #tags=['ACTORS_TYPE']
    for webentity in csv.DictReader(f) :
      # Get the necessary info from CSV
      status = webentity['STATUS']
      if webentity['STATUS'] == 'IN':
        tagIndex[webentity['ID']] = {}

        for tag in tags:
          tagIndex[webentity['ID']][tag] = webentity[tag]
  return tagIndex

def addTagAttributesDef(array, tag):
  string = '<attribute id="attr_tag_%s" title="%s" type="string"></attribute>\n' % (tag, tag)
  array.append(string)

def addAllTagsAttributesDef(array):
  for tag in tags:
    addTagAttributesDef(array, tag)

def addTagAttributes(array, tagIndex, we):
  for tag in tags:
    string = '<attvalue for="attr_tag_%s" value="%s"></attvalue>\n' % (tag, tagIndex[we][tag])
    array.append(string)

def runThroughGexf():
  tagIndex = createTagIndex()
  linesGexfBase = readGexf()
  linesGexfNew = []
  inNodes = False
  p = re.compile('(?<=<node id=")([\w-]*)')
  currentNode = ''
  for line in linesGexfBase:
    linesGexfNew.append(line)
    # Adds all the attributes to the node definition
    if (line == '<attributes class="node" mode="static">\n'):
      addAllTagsAttributesDef(linesGexfNew)
      inNodes = True
    elif (line == '<edges>\n'):
      inNodes = False
    else :
      if (inNodes):
        matchNode = '' if (p.search(line) is None) else p.search(line).group(0)
        if (matchNode in tagIndex):
          currentNode = matchNode
        elif (line == '<attvalues>\n'):
          addTagAttributes(linesGexfNew, tagIndex, currentNode)


  return linesGexfNew

def exportFile(file, arrayOfStrings):
  if not os.path.exists(graphExportFolder):
    os.makedirs(graphExportFolder)
  with open(graphExportFolder + file, 'w') as outfile:
    string = ''.join(arrayOfStrings)
    outfile.write(string)

if __name__=='__main__':
  exportFile('graph.gexf', runThroughGexf())
  # readGexf()
