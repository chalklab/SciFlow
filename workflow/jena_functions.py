import requests
import urllib3
from sciflow import localsettings

path = "http://jena1.unfcsd.unf.edu:3030/"
dset = "SciData"
hdrs = {'Content-type': 'application/json'}
hdrsld = {'Content-type': 'application/ld+json'}
fpath = localsettings.ppath + "/static/files/"


def server():
    """get the server info from the fuseki endpoint"""
    endpoint = path + "$/server"
    response = requests.get(endpoint, headers=hdrs, auth=(localsettings.fuser, localsettings.fpass)).json()
    return response['version']


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
    else:
        """ assumes file is in <prjroot>/static/files/ """
        with open(fpath + file) as fp:
            data = fp.read()
    endpoint = path + dset + "/upload"
    response = requests.post(endpoint, data=data, headers=hdrsld, auth=(localsettings.fuser, localsettings.fpass))
    return response
