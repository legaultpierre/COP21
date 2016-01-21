# Solr extraction scripts

## extractDataFromServer.py
Contains the functions to get the data from solr.  
You should NOT call this file.

## extractWordOccurBy******ByLrus.py where ****** = Tags or We
Generates the json files by tags or web entity.

### Requirements
The folders `indexesByWE` and `indexedByTag` have to be created inside the `extractedData` folder


## mostEmployedWords.py
Generate json files inside the `extractedData/topWords`

### Use
`python mostEmployedWords.py arg` where arg = 0 for tags and arg = 1 for web entity

### Requirements
1. The folder `topWords` has to be created inside the `extractedData` folder
2. The folders `indexesByWE` and `indexedByTag` have to be created inside the `extractedData/topWords` folder
3. Needs the `extractWordOccurBy******ByLrus.py` to be run before


## convertWordOccurJsonToCsv.py
Generate CSV from the `extractedData/topWords` files

### Requirements
1. The folder `topWords` has to be created inside the `extractedData` folder
2. The folders `csvFiles` have to be created inside the `extractedData/topWords/` folder
3. Needs the `extractWordOccurBy******ByLrus.py` to be run before


## linkWEbyWordCooccurence.py
Generate the wordIndexLinksWithWE.json

### Requirement
Needs the `extractWordOccurBy******ByLrus.py` to be run before

## convertLinkWEbyWordCoocuFromJsonToGDF.py
Generate graph file of word coocurences for web entities

### Requirement
Needs the `convertLinkWEbyWordCoocuFromJsonToGDF.py` to be run before
