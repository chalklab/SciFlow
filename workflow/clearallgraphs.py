""" clear all graphs in the DB """
import os
import django
import jena_functions

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

# resp = jena_functions.addgraph("chemtwin_AAAQKTZKLRYKHR-UHFFFAOYSA-N.jsonld")
# resp = jena_functions.addgraph("chemtwin_AABBLHFMQYNECK-NRFANRHFSA-N.jsonld")
# search for all graphs
sparql = "SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o }}"
resp = jena_functions.query(sparql)

# get list of all graphs
graphs = []
for graph in resp['results']['bindings']:
    graphs.append(graph['g']['value'])
# print(graphs)
# exit()

# DROP each graph
for graph in graphs:
    sparql = "DROP GRAPH <" + graph + ">"
    deleted = jena_functions.update(sparql)
    if deleted:
        print("Graph '" + graph + "' deleted")

# clear default graph of two triples per JSON-LD file
sparql = "CLEAR GRAPH <>"
deleted = jena_functions.update(sparql)
if deleted == "success":
    print("Default graph triples deleted")
else:
    print(deleted)
exit()
