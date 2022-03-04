"""example functionality for testing"""
import os
import django
import requests
import jena_functions

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

resp = jena_functions.sparql()
print(resp)
exit()


resp = jena_functions.addgraph("/Users/n00002621/Desktop/chemtwins/facet00000001.jsonld")
print(resp)
exit()


data = open('/Users/n00002621/Desktop/chemtwins/facet00000001.jsonld').read()

# Set path to file to be posted
headers = {'Content-Type': 'application/ld+json'}

# Modify header to match content type (see below)
response = requests.post('http://jena1.unfcsd.unf.edu:3030/SciData/data?default', data=data, headers=headers)

# Point request to Fuseki "data" endpoint; append graph name (currently default)
current_url = response.text
print(response.text)

# Possible filetypes/headers:
# n3: text/n3; charset=utf-8
# nt: text/plain
# rdf: application/rdf+xml
# owl: application/rdf+xml
# nq: application/n-quads
# trig: application/trig
# jsonld: application/ld+json


# basedir = settings.BASE_DIR
# fpath = basedir + '/static/files/240_72215_2324256.jsonld'
# with open(fpath) as f:
#     json = json.load(f)
# test = jsonld.to_rdf(json, {"processingMode": "json-ld-1.0"})
# print(test)
