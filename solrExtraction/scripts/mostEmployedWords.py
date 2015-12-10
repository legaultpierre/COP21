# utils
import re, sys

# data sources
import sunburnt
import json

# Creates an object that will contain all the data retrieved
index = {}

# Contains all the Solr, Hyphe and Mongo conf
conf = {}

# Contains the solr method to execute
solrCriteria = {
  'language': 'EN'
}

# Translate the solr criteria object into a valid sunburnt request
def translateToSunburnt(solr, solrCriteria):
  return solr.query(**solrCriteria)

# Loads the Solr, Hyphe, Mongo configuration into conf
def loadConf():
  #Load conf
  try:
    with open('../../hyphe2solr_modified/config.json') as confile:
      conf = json.loads(confile.read())
      return conf
  except Exception as e:
    sys.stderr.write("%s: %s\n" % (type(e), e))
    sys.stderr.write('ERROR: Could not read configuration\n')
    sys.exit(1)

# Calls the given solr method
def getSolrResults(conf, solrCriteria):
  adress = "http://%s:%s/solr/%s" % \
    (conf['solr']['host'], conf['solr']['port'],
    get_solr_instance_name(conf['solr']['path']))
  try:
    solr = sunburnt.SolrInterface(adress)
  except Exception as e:
    sys.stderr.write("%s: %s\n" % (type(e), e))
    sys.stderr.write('ERROR: Could not initiate connection to SOLR node\n')
    sys.exit(1)

  try:
    result = translateToSunburnt(solr, solrCriteria).execute()
    return result
  except Exception as e:
    sys.stderr.write("%s: %s\n" % (type(e), e))
    sys.stderr.write('ERROR: Could retrieve data from Solr\n')
    sys.exit(1)

# utils
re_solrname = re.compile(r"^.*/([^/]+)$")
get_solr_instance_name = lambda solrpath: re_solrname.sub(r"\1", solrpath)

if __name__=='__main__':
  conf = loadConf()
  print getSolrResults(conf, solrCriteria)
