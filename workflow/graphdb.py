""" wrapper definitions to the GraphDB API - note that named graphs are referred to as contexts in RDF4J """
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
