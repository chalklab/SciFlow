""" settings for the workflow """

# headers for files
jsonhrs = {'Content-type': 'application/json', 'Accept': 'application/json'}

# list of strings to find in the metadata names, to identify important identifiers to search on
searchterms = {
    "compound": ['name', 'inchi', 'smiles', 'chembl', 'pubchem', 'wiki'],
    "target": ['name', 'chembl']
}

# graphdb paths
graphserverurl = 'http://localhost:7201/'
graphreponame = 'scidata'
graphuploadlocalurl = graphserverurl + 'rest/data/import/server/' + graphreponame
graphuploadremoteurl = graphserverurl + 'rest/data/upload/server/' + graphreponame + '/url/'
graphsparqlurl = graphserverurl + 'repositories/' + graphreponame

sdsnewpath = "/Users/Shared/sciflow"
