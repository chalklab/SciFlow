""" settings for the workflow """

# headers for files
jsonhrs = {'Content-type': 'application/json', 'Accept': 'application/json'}

# list of strings to find in the metadata names,
# to identify important identifiers to search on
searchterms = {
    "compound": ['name', 'inchi', 'smiles', 'chembl', 'pubchem', 'wiki'],
    "target": ['name', 'chembl']
}

# graphdb paths
reponame = 'scidata'
graphsdspath = 'http://localhost:7201/'
graphsdsurl = graphsdspath + 'rest/data/import/upload/' + reponame + '/url'
graphsparqlsdsurl = graphsdspath + 'repositories/' + reponame

graphlocalpath = 'http://localhost:7200/'
graphlocalurl = graphlocalpath + 'rest/data/import/upload/' + reponame + '/url'
graphsparqllocalurl = graphlocalpath + 'repositories/' + reponame

sdsnewpath = "/Users/Shared/sciflow"
