import requests
import urllib3
import json
from sciflow import localsettings


path = "http://jena1.unfcsd.unf.edu:3030/"
dataset = "SciData"
hdrs = {'Content-Type': 'application/json'}
hdrsld = {'Content-Type': 'application/ld+json'}
fpath = localsettings.ppath + "/static/files/"


def server():
    """get the server info from the fuseki endpoint"""
    endpoint = path + "$/server"
    response = requests.get(endpoint, headers=hdrs, auth=(localsettings.fuser, localsettings.fpass)).json()
    return response


def stats():
    endpoint = path + "$/stats"
    return requests.get(endpoint, headers=hdrs, auth=(localsettings.fuser, localsettings.fpass)).json()


def listsets():
    endpoint = path + "$/datasets"
    response = requests.get(endpoint, headers=hdrs, auth=(localsettings.fuser, localsettings.fpass))
    jsn = response.content.decode('utf-8')
    dsets = json.loads(jsn)
    output = []
    for dset in dsets['datasets']:
        output.append(dset['ds.name'].replace('/', ''))
    return output


def compact(dset=dataset):
    endpoint = path + "$/compact/" + dset + "?deleteOld=true"
    return requests.post(endpoint, headers=hdrs, auth=(localsettings.fuser, localsettings.fpass)).json()


def setstats(dset=dataset):
    """get the status of the SciData dataset from the fuseki endpoint"""
    endpoint = path + "$/stats/" + dset
    response = requests.get(endpoint, headers=hdrs, auth=(localsettings.fuser, localsettings.fpass)).json()
    return response


def status(dset=dataset):
    """get the stats of the SciData dataset from the fuseki endpoint"""
    endpoint = path + "$/datasets/" + dset
    response = requests.get(endpoint, headers=hdrs, auth=(localsettings.fuser, localsettings.fpass)).json()
    return response['ds.state']


def query(sparql, dset=dataset, fixes=None):
    """ executes a SPARQL query """
    stdfixes = "PREFIX wdt: <http://www.wikidata.org/prop/direct/>"
    sparql = stdfixes + " " + sparql
    if fixes:
        sparql = fixes + " " + sparql
    endpoint = path + dset + "/sparql"
    return requests.post(endpoint, data={'query': sparql}, auth=(localsettings.fuser, localsettings.fpass))


def update(sparql, dset=dataset):
    """ executes a SPARQL query """
    endpoint = path + dset + "/update"
    response = requests.post(endpoint, data={'update': sparql}, auth=(localsettings.fuser, localsettings.fpass))
    if response.status_code == 200:
        return "success"
    else:
        return response.text


def deldataset(dset=None):
    dsets = listsets()
    if dset:
        if dset in dsets:
            """ clear the dataset """
            cleardataset(dset)
            """ delete the dataset """
            endpoint = path + "$/datasets/" + dset
            response = requests.delete(endpoint, auth=(localsettings.fuser, localsettings.fpass))
            if response.status_code == 200:
                return response.content  # is empty binary string
            else:
                return "error executing deletion: " + str(response.status_code)
        else:
            return 'invalid dataset'
    else:
        return 'no dataset'


# special functions
def tcount():
    """ count all triples in the dataset """
    ncount, dcount = 0, 0

    # across all named graphs
    sparql = "SELECT (COUNT(?s) AS ?triples) WHERE { GRAPH ?g { ?s ?p ?o . }}"
    out = query(sparql)
    if out.status_code == 200:
        jsn = out.content.decode('utf-8')
        data = json.loads(jsn)
        ncount = int(data['results']['bindings'][0]['triples']['value'])

    # in default graph
    sparql = "SELECT (COUNT(?s) AS ?triples) WHERE {  ?s ?p ?o . }"
    out = query(sparql)
    if out.status_code == 200:
        jsn = out.content.decode('utf-8')
        data = json.loads(jsn)
        dcount = int(data['results']['bindings'][0]['triples']['value'])
    # all triples
    acount = dcount + ncount
    return acount


def jenaadd(file, replace="", dset=dataset):
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
    # remove existing version of graph if presente
    if replace != "":
        sparql = "CLEAR GRAPH <" + replace + ">"
        print(sparql)
        result = update(sparql)
        print(result)
    # create endpoint URL
    endpoint = path + dset + "/data"
    response = requests.post(endpoint, data=data, headers=hdrsld, auth=(localsettings.fuser, localsettings.fpass))
    if response.status_code == 200:
        return "success"
    else:
        return response.text


def delgraph(graph, dset=dataset):
    qry = "DROP GRAPH <" + graph + ">"
    output = update(qry, dset)
    return output


def cleardataset(dset=None):
    if dset:
        # get list of all graph names as JSON
        fix = "PREFIX obo: <http://purl.obolibrary.org/obo/>"
        qry = 'SELECT DISTINCT ?g WHERE {GRAPH ?g { ?s ?p ?o . }}'
        sparql = fix + " " + qry
        out = query(sparql, dset)
        if out.status_code == 200:
            jsn = out.content.decode('utf-8')
            graphs = json.loads(jsn)
            # iterate over all graphs and delete
            for graph in graphs['results']['bindings']:
                resp = delgraph(graph['g']['value'], dset)
                print("deleted " + graph['g']['value'])
    return "success"
