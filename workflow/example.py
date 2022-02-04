"""example functionality for testing"""
import os
import django
import requests
import jena_functions

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

# if I run either of these I get a <Response [400]> :(
# resp = jena_functions.addgraph("https://sds.coas.unf.edu/sciflow/files/facet/2")
resp = jena_functions.addgraph("chemtwin2_GZKLJWGUPQBVJQ-UHFFFAOYSA-N.jsonld")
print(resp)
exit()


data = open('/Users/n00002621/Desktop/trc070121/je034134e_2.jsonld').read()

# Set path to file to be posted
headers = {'Content-Type': 'application/ld+json'}

# Modify header to match content type (see below)
response = requests.post('http://139.62.166.57:3030/TRC_TBD2/data?default', data=data, headers=headers)

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
