""" wrapper definitions to the GraphDB API """
from urllib.parse import quote
from workflow.settings import *
from substances.models import *
from django.db import *
from workflow.log_functions import *
from sciflow.settings import *
import json
import requests


def addgraph(ftype, fid, locale='local', replace=""):
    """ add a file to GraphDB """
    fileurl = "https://sds.coas.unf.edu/sciflow/files/" + ftype + '/' + str(fid)
    if replace != "":
        data = '{"data":"' + fileurl + '","replaceGraphs":["' + replace + '"]}'
    else:
        data = '{ "data": "' + fileurl + '" }'
    file = open(BASE_DIR + '/static/replacelog.txt', 'a+')
    file.write(data + '\r\n')
    file.close()

    r = None
    if locale == "local":
        r = requests.post(graphlocalurl, data=data, headers=jsonhrs)
        actlog("GDB_A01: Added local graph (" + str(r) + ")")
    elif locale == 'remote':
        r = requests.post(graphsdsurl, data=data, headers=jsonhrs)
        actlog("GDB_A02: Added remote graph (" + str(r) + ")")
    else:
        actlog("GDB_A03: Locale not one of 'local' or 'remote'")

    # return outcome of addition
    return r.ok


def isgraph(name, locale='local'):
    """ check to see if a named graph is present in GraphDB """
    headers = {'Accept': 'application/sparql-results+json'}
    params = {'query': 'ASK WHERE { GRAPH <' + name + '> { ?s ?p ?o } }'}

    # response format { "head" : { }, "boolean" : true }
    url = ""
    if locale == 'local':
        url = graphsparqllocalurl
    elif locale == 'remote':
        url = graphsparqlsdsurl
    response = requests.get(url, headers=headers, params=params).json()
    if response['boolean']:
        return True
    else:
        return False


def getgraphname(identifier, locale='local'):
    """ get the name of a named graph using substring """
    headers = {'Accept': 'application/sparql-results+json'}
    params = {
        'query': 'SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o. } FILTER(contains(str(?g),"' + identifier + '"))}'}
    # response format {'head': {'vars': ['g']}, 'results': {'bindings': [{'g':
    # {'type': 'uri', 'value': <graphname>}}]}}
    url = graphsparqlsdsurl  # default to Graph DB on SDS
    if locale == 'local':
        url = graphsparqllocalurl
    response = requests.get(url, headers=headers, params=params).json()
    return response['results']['bindings'][0]['g']['value']


# misc
def graphsize(repo):
    """ get /rest/repositories/{repositoryID}/size
        get the size of the graph"""
    headers = {'Accept': 'application/json'}
    r = requests.get("http://localhost:7200/rest/repositories/" + repo + "/size",
                     headers=headers)
    print(r.text)


def graphdownload(repo):
    """ get /rest/repositories/{repositoryID}/download
        downloads the graph """
    headers = {'Accept': 'application/json'}
    r = requests.get("http://localhost:7200/rest/repositories/" + repo + "/download",
                     headers=headers)
    # TODO: Make it so this actually writes a file instead of printing
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
    r = requests.get("http://localhost:7200/repositories/" + repo + "/contexts",
                     headers=headers)
    print(r.text)


# statements
def graphstatementsget(graph, repo):  # TODO: ???
    """ get /repositories/{repositoryID}
        gets all statements of a given graph """
    headers = {'Accept': 'text/plain'}
    r = requests.get("http://localhost:7200/repositories/" + repo + "/rdf-graphs/" + graph,
                     headers=headers)
    print(r.text)


def graphstatementedit(baseuri, update, repo):  # DONE??
    """ put /repositories/{repositoryID}/statements
        updates a statement in the repo """
    headers = {'Content-type': ' application/rdf+xml', 'Accept': 'text/plain'}
    r = requests.get("http://localhost:7200/repositories/" + repo + "/statements?update=" + update + "&baseURI=" + baseuri,
                     headers=headers)
    print(r.text)


# queries
def graphqueryrun(query, repo):
    """ get /repositories/{repositoryID}
    runs a query """
    headers = {'Accept': 'application/sparql-results+json'}
    r = requests.get("http://localhost:7200/repositories/" + repo + "?query=" + quote(query),
                     headers=headers)
    print(r.text)
    print(r)


def graphqueryget():
    """ get /rest/sparql/saved-queries
    gets queries """
    headers = {'Accept': 'application/json'}
    r = requests.get("http://localhost:7200/rest/sparql/saved-queries",
                     headers=headers)
    # TODO: It prints but it doesn't look nice
    print(json.loads(r.text))


def graphqueryedit(query):
    """ put /rest/sparql/saved-queries
    edit a query preset """
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'}
    data = '{\n "data": ' + query + ' \n }'
    r = requests.put("http://localhost:7200/rest/sparql/saved-queries",
                     data=data, headers=headers)
    print(r.text)


def graphquerycreate(newquery):
    """ post /rest/sparql/saved-queries
    create a query preset """
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'}
    data = '{\n "data": ' + newquery + ' \n }'
    r = requests.post("http://localhost:7200/rest/sparql/saved-queries",
                      data=data, headers=headers)
    print(r.text)


def graphquerydelete(query):
    """ deletes a query preset """
    headers = {'Accept': 'application/json'}
    r = requests.delete("http://localhost:7200/rest/sparql/saved-queries?name=" + query,
                        headers=headers)
    print(r.text)


# namespaces
def graphnamespaceget(prefix, repo):
    """ get /repositories/{repositoryID}/namespaces/{namespacesPrefix}
        gets a namespace prefix """
    headers = {'Accept': 'text/plain'}
    r = requests.get("http://localhost:7200/repositories/" + repo + "/namespaces/" + prefix,
                     headers=headers)
    print(r.text)


# TODO: Can't see the format currently
def graphnamespacecreate(uri, prefix, repo):
    """ put /repositories/{repositoryID}/namespaces/{namespacesPrefix}
        creates a namespace prefix """
    print(uri, prefix, repo)


def graph_link_a(file):
    """graph link a function"""
    jsonfile = json.load(file)
    try:
        for group in jsonfile['@graph']['scidata']['system']['facets']:
            if group['@id'].startswith(('compound/', 'crystal/')):
                newgroup = graph_link_b(group)
                group.clear()
                group.update(newgroup)
                actlog("GDB_05: Graph Link Group: " + group)
    except DataError:
        errorlog("GDB_06: Problem finding facets in file")
    return jsonfile


def graph_link_b(group):
    """graph link b function"""
    # group = {'@id': 'compound/1/', '@type': 'cif:compound',
    # '_chemical_formula_moiety': 'C12 H8',
    # '_chemical_name_systematic': 'Q194207'}
    tablematch = {
        "compound": [Identifiers, Substances, 'substance_id'],
        "crystal": [Identifiers, Substances, 'substance_id']}
    identifier = {'@id': group['@id']}
    category = group['@id'].split('/')[0]
    for line in list(tablematch[category][0].objects.values()):
        try:
            if any(line['value'] in q for q in group.values()):
                if line['value'] in group.values():
                    group = identifier
                    group.update(tablematch[category][1].objects.values(
                        'graphdb').get(id=line[tablematch[category][2]]))
                    # Post(y)
            else:
                # compound/crystal/etc not found in database
                # Needs to be added first in order to link
                # then GraphLinkB(group)
                pass
        except ValueError:
            errorlog("GDB_04: Problem with matching data in group.values()")
    return group
