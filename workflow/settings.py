""" settings for the workflow """

# headers for files
jsonhrs = {'Content-type': 'application/json', 'Accept': 'application/json'}

# list of strings to find in the metadata names, to identify important identifiers to search on
searchterms = {
    "compound": ['name', 'inchi', 'smiles', 'chembl', 'pubchem', 'wiki'],
    "target": ['name', 'chembl']
}

# graphdb paths
graphreponame = 'scidata'
graphsdspath = 'http://localhost:7201/'
graphsdsurl = graphsdspath + 'rest/data/import/upload/' + graphreponame + '/url'
graphsparqlsdsurl = graphsdspath + 'repositories/' + graphreponame

graphlocalpath = 'http://localhost:7200/'
graphlocalurl = graphlocalpath + 'rest/data/import/upload/' + graphreponame + '/url'
graphsparqllocalurl = graphlocalpath + 'repositories/' + graphreponame

sdsnewpath = "/Users/Shared/sciflow"
