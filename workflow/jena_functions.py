import requests
import urllib3
from sciflow import localsettings


path = "http://jena1.unfcsd.unf.edu:3030/"
dset = "SciData"
hdrs = {'Content-Type': 'application/json'}
hdrsld = {'Content-Type': 'application/ld+json'}
fpath = localsettings.ppath + "/static/files/"


def server():
    """get the server info from the fuseki endpoint"""
    endpoint = path + "$/server"
    response = requests.get(endpoint, headers=hdrs, auth=(localsettings.fuser, localsettings.fpass)).json()
    return response


def stats():
    """get the status of the SciData dataset from the fuseki endpoint"""
    endpoint = path + "$/stats/" + dset
    response = requests.get(endpoint, headers=hdrs, auth=(localsettings.fuser, localsettings.fpass)).json()
    return response


def status():
    """get the stats of the SciData dataset from the fuseki endpoint"""
    endpoint = path + "$/datasets/" + dset
    response = requests.get(endpoint, headers=hdrs, auth=(localsettings.fuser, localsettings.fpass)).json()
    return response['ds.state']


def addgraph(file):
    """ add a file to Jena """
    if "http" in file:
        http = urllib3.PoolManager()
        r = http.request('GET', file)
        data = r.data
    elif file[0] == "/":
        """ assumes file is full local path """
        with open(file) as fp:
            data = fp.read()
    else:
        """ assumes file is in <prjroot>/static/files/ """
        with open(fpath + file) as fp:
            data = fp.read()
    # create endpoint URL
    endpoint = path + dset + "/data"
    response = requests.post(endpoint, data=data, headers=hdrsld, auth=(localsettings.fuser, localsettings.fpass))
    if response.status_code == 200:
        return "success"
    else:
        return response.text


def query(sparql):
    """ executes a SPARQL query """
    endpoint = path + dset + "/sparql"
    response = requests.post(endpoint, data={'query': sparql}, auth=(localsettings.fuser, localsettings.fpass))
    return response.json()


def update(sparql):
    """ executes a SPARQL query """
    endpoint = path + dset + "/update"
    response = requests.post(endpoint, data={'update': sparql}, auth=(localsettings.fuser, localsettings.fpass))
    if response.status_code == 200:
        return "success"
    else:
        return response.text


# special functions
def tcount():
    """ count all triples in the dataset """
    # across all named graphs
    sparql = "SELECT (COUNT(?s) AS ?triples) WHERE { GRAPH ?g { ?s ?p ?o . }}"
    out = query(sparql)
    ncount = int(out['results']['bindings'][0]['triples']['value'])
    # in default graph
    sparql = "SELECT (COUNT(?s) AS ?triples) WHERE {  ?s ?p ?o . }"
    out = query(sparql)
    dcount = int(out['results']['bindings'][0]['triples']['value'])
    # all triples
    acount = dcount + ncount
    return acount
