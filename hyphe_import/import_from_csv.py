# -*- coding: utf-8 -*-

#
# Libs
#
import jsonrpclib
import csv
import sys
import logging

#
# Config
#
corpus = 'legaultpierre'
password = ''
log_file = 'start_crawling_webentities_from_csv.log'
log_level = logging.DEBUG
webentities_file = 'COP21.csv'
depth_crawl = 1
phantom_crawl = False
# Should be of this format : 'http://hyphe.medialab.sciences-po.fr/INSTANCE-api/'
# if you usually access Hyphe from : 'http://hyphe.medialab.sciences-po.fr/INSTANCE/'
api_url = 'http://hyphe.medialab.sciences-po.fr/demo-api/'

#
# Programm
#
logging.basicConfig(filename = log_file, filemode = 'w', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
logging.info('start')

def main():
  # Connect to the Hyphe - API
  try :
    hyphe_core = jsonrpclib.Server(api_url, version = 1)
    logging.info('Connection success')
  except Exception as e :
    logging.error('Could not initiate connection to hyphe core')
    sys.exit(1)
  # Be sure that the corpus is started
  result = hyphe_core.start_corpus(corpus, password)
  if result['code'] == 'fail' :
    logging.error(result['message'])
    sys.exit(1)
  # Reset the corpus
  hyphe_core.reinitialize(corpus)

  if result['code'] == 'fail' :
    logging.error(result['message'])
  else :
    logging.info(result['result'])

  # Iterate over the web entities
  with open(webentities_file) as f :
    for webentity in csv.DictReader(f) :
      # Get the necessary info from CSV
      prefixesAsUrls = convertSpaceSeparatedValueToArray(webentity['PREFIXES'])
      name = webentity['NAME']
      status = webentity['STATUS']
      startPages = convertSpaceSeparatedValueToArray(webentity['START PAGES'])
      wantedId = webentity['ID'];

      # Add web entities to corpus
      result = hyphe_core.store.declare_webentity_by_lrus_as_urls(prefixesAsUrls, name, status, startPages, corpus)
      # if result['code'] == 'fail' :
      #   logging.error(result['message'])
      # else :
      #   logging.info(result['result'])

      # Gets the newly created web entity
      remoteWebEntity = hyphe_core.store.get_webentity_for_url(prefixesAsUrls[0], corpus)
      if remoteWebEntity['code'] == 'fail':
        logging.error(remoteWebEntity['message'])
      else :
        # logging.info(remoteWebEntity['result'])
        remoteWebEntity = remoteWebEntity['result']
        # Sets the web entity id to the one present in the CSV file
        result = hyphe_core.store.change_webentity_id(remoteWebEntity['id'], wantedId, corpus)
        # if result['code'] == 'fail' :
        #   logging.error(result['message'])
        # else :
          # logging.info(result['result'])

      # For all web entities, reset the status to the one of the .csv file
      result = hyphe_core.store.set_webentity_status(webentity['ID'], webentity['STATUS'], corpus)

      #Add the web entity to be crawled, if it STATUS is 'IN' and it has not been crawled before, ie. CRAWLING STATUS is 'UNCRAWLED'
      if webentity['STATUS'] == 'IN':
        result = hyphe_core.crawl_webentity_with_startmode(webentity['ID'], depth_crawl, phantom_crawl, webentity['STATUS'], ["startpages", "prefixes"], {}, corpus)
        if result['code'] == 'fail' :
          logging.error(result['message'])
        # else :
          # logging.info(result['result'])

def convertSpaceSeparatedValueToArray(string):
  if string == '':
    return []
  else :
    return string.split(' ')

if __name__ == '__main__':
  main()
