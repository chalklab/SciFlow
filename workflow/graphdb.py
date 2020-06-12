""" wrapper definitions to the GraphDB API """
import requests


def add(file):
    """ add a file to GraphDB"""
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    x = '"{}"'.format(file)
    data = '{\n "data": ' + x + ' \n }'
    r = requests.post("http://localhost:7201/rest/data/import/upload/scidata/url", data=data, headers=headers)
    print(r)


# add("https://stuchalk.github.io/scidata/examples/cif/1000118.jsonld")
