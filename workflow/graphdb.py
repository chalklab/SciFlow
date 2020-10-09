""" wrapper definitions to the GraphDB API """
import json
from urllib.parse import quote
from workflow.settings import *
import requests


def addgraph(file, locale):
    """ add a file to GraphDB """
    data = '{"fileNames": ["' + file + '"]}'
    if locale == "local":
        r = requests.post(graphuploadlocalurl, data=data, headers=jsonhrs)
    elif locale == 'remote':
        r = requests.post(graphuploadremoteurl, data=data, headers=jsonhrs)
    else:
        return False
    return r.ok


def isgraph(name):
    """ check to see if a named graph is present in GraphDB """
    headers = {'Accept': 'application/sparql-results+json'}
    params = {'query': 'ASK WHERE { GRAPH <' + name + '> { ?s ?p ?o } }'}

    # response format { "head" : { }, "boolean" : true }
    temp = graphsparqlurl
    response = requests.get(temp, headers=headers, params=params).json()
    if response['boolean']:
        return True
    else:
        return False


def getgraphname(identifier):
    """ get the name of a named graph using substring """
    headers = {'Accept': 'application/sparql-results+json'}
    params = {'query': 'SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o. } FILTER(contains(str(?g),"'+identifier+'"))}'}
    # response format {'head': {'vars': ['g']}, 'results': {'bindings': [{'g': {'type': 'uri', 'value': <graphname>}}]}}
    temp = graphsparqlurl
    response = requests.get(temp, headers=headers, params=params).json()
    return response['results']['bindings'][0]['g']['value']


def graphadd(file, repo):
    """ post /rest/data/import/upload/{repositoryID}/url
        add a file to GraphDB """
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    x = '"{}"'.format(file)
    data = '{\n "data": ' + x + ' \n }'
    r = requests.post("http://localhost:7200/rest/data/import/upload/"+repo+"/url", data=data, headers=headers)
    print(r.text)


# misc
def graphsize(repo):
    """ get /rest/repositories/{repositoryID}/size
        get the size of the graph"""
    headers = {'Accept': 'application/json'}
    r = requests.get("http://localhost:7200/rest/repositories/"+repo+"/size", headers=headers)
    print(r.text)


def graphdownload(repo):  # TODO: Make it so this actually writes a file instead of printing
    """ get /rest/repositories/{repositoryID}/download
        downloads the graph """
    headers = {'Accept': 'application/json'}
    r = requests.get("http://localhost:7200/rest/repositories/"+repo+"/download", headers=headers)

    print(r.text)


def graphrepos():
    """ get /repositories
        gets repos """
    headers = {'Accept': 'application/sparql-results+json'}
    r = requests.get("http://localhost:7200/repositories", headers=headers)
    print(r.text)


def graphcontexts(repo):
    """ get /repositories/{repositoryID}/contexts
        gets context """
    headers = {'Accept': 'application/sparql-results+json'}
    r = requests.get("http://localhost:7200/repositories/"+repo+"/contexts", headers=headers)
    print(r.text)


# statements
def graphstatementsget(graph, repo):  # TODO: ???
    """ get /repositories/{repositoryID}
        gets all statements of a given graph """
    headers = {'Accept': 'text/plain'}
    r = requests.get("http://localhost:7200/repositories/"+repo+"/rdf-graphs/"+graph, headers=headers)
    print(r.text)


def graphstatementedit(baseuri, update, repo):  # DONE??
    """ put /repositories/{repositoryID}/statements
        updates a statement in the repo """
    headers = {'Content-type': ' application/rdf+xml', 'Accept': 'text/plain'}
    r = requests.get("http://localhost:7200/repositories/"+repo+"/statements?update="+update+"&baseURI="+baseuri, headers=headers)
    print(r.text)


# queries
def graphqueryrun(query, repo):
    """ get /repositories/{repositoryID}
    runs a query """
    headers = {'Accept': 'application/sparql-results+json'}
    r = requests.get("http://localhost:7200/repositories/"+repo+"?query="+quote(query), headers=headers)
    print(r.text)
    print(r)


def graphqueryget():  # TODO: It prints but it doesn't look nice
    """ get /rest/sparql/saved-queries
    gets queries """
    headers = {'Accept': 'application/json'}
    r = requests.get("http://localhost:7200/rest/sparql/saved-queries", headers=headers)
    print(json.loads(r.text))


def graphqueryedit(query):
    """ put /rest/sparql/saved-queries
    edit a query preset """
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    data = '{\n "data": ' + query + ' \n }'
    r = requests.put("http://localhost:7200/rest/sparql/saved-queries", data=data, headers=headers)
    print(r.text)


def graphquerycreate(newquery):
    """ post /rest/sparql/saved-queries
    create a query preset """
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    data = '{\n "data": ' + newquery + ' \n }'
    r = requests.post("http://localhost:7200/rest/sparql/saved-queries", data=data, headers=headers)
    print(r.text)


def graphquerydelete(query):
    """ deletes a query preset """
    headers = {'Accept': 'application/json'}
    r = requests.delete("http://localhost:7200/rest/sparql/saved-queries?name="+query, headers=headers)
    print(r.text)


# namespaces
def graphnamespaceget(prefix, repo):
    """ get /repositories/{repositoryID}/namespaces/{namespacesPrefix}
        gets a namespace prefix """
    headers = {'Accept': 'text/plain'}
    r = requests.get("http://localhost:7200/repositories/"+repo+"/namespaces/"+prefix, headers=headers)
    print(r.text)


def graphnamespacecreate(uri, prefix, repo): #TODO: Can't see the format currently
    """ put /repositories/{repositoryID}/namespaces/{namespacesPrefix}
        creates a namespace prefix """
    print(prefix)

