"""
    backend
    1) Load JSON-LD (workflow.ingestion)
    2) Check if compound is already present in SQL DB (substances.*)
    3) Scrape for compound data (substances.sources)
    4) Add compound to SQL DB (substances.*)
    5) Check if compound is already present in GraphDB and add if not
    6) Process JSON-LD to add links to GraphDB (workflow.graph_link)
    7) Add JSON-LD to GraphDB (workflow.graphdb)

    frontend
    1) Views
    ) Manually add compounds
"""

"""crosswalks"""

"""datasets"""

# from datasets.ds_functions import *
# getdatasetnames
# getsourcecodes
# getcodesnames

"""substances"""

# from substances.sub_functions import *
#  addsubstance
#  getidtype
#  getsubdata
#  pubchemkey
#  createsubjld
#  get_item
#  get_items
#  saveids
#  savedescs

# from substances.mysql import *
# getsubid
# ingraph
# getinchikey
# addsubgraphname
# updatesubstancefield
# clearsubstancefield
# addidentifier
# createsubstance
# subsearch

# from substances.external import *
# pubchem
# classyfire
# wikidata
# chembl
# pubchemsyns

"""users"""

# from users.requests import *
# makerequest
# rejectrequest
# approverequest

"""workflow"""

# from workflow.gdb_functions import *
#     Post
#     GraphLinkA
#     GraphLinkB
#
#     addgraph
#     isgraph
#     getgraphname
#     graphsize
#     graphdownload
#     graphrepos
#     graphcontexts
#     graphstatementsget
#     graphstatementedit
#     graphqueryrun
#     graphqueryget
#     graphqueryedit
#     graphquerycreate
#     graphquerydelete
#     graphnamespaceget
#     graphnamespacecreate

# from workflow.wf_functions import *
#     #ingestion
#     ingest

#     #normalization
#     normalize
#     getfacet

#     from datafiles.validation import *
#     validate
#     check_type
