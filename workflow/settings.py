""" settings for the workflow """
import pathlib
from sciflow.settings_local import gdrive
# 1. go to the sciflow google drive, select it, and press shift + z
# 2. sync this folder to your computer
# 3. put your root path as the defined root path, then add this file to gitignore

root_path = gdrive

# directories:

# TODO These should be generic

# herg
hergautoinput = pathlib.Path(root_path + '/herg/00 herg auto input')
herginput = pathlib.Path(root_path + '/herg/01 herg input')
hergoutput = pathlib.Path(root_path + '/herg/02 herg output')
hergerror = pathlib.Path(root_path + '/herg/03 herg error')
herglog = pathlib.Path(root_path + '/herg/04 herg log')

# cif
cifautoinput = pathlib.Path(root_path + '/cif/00 cif auto input')
cifinput = pathlib.Path(root_path + '/cif/01 cif input')
cifoutput = pathlib.Path(root_path + '/cif/02 cif output')
ciferror = pathlib.Path(root_path + '/cif/03 cif error')
ciflog = pathlib.Path(root_path + '/cif/04 cif log')

# headers for files
jsonhrs = {'Content-type': 'application/json', 'Accept': 'application/json'}

# list of strings to find in the metadata names, to identify important identifiers to search on
searchterms = {
    "compound": ['name', 'inchi', 'smiles', 'chembl', 'pubchem', 'wiki'],
    "target": ['name', 'chembl']
}

# graphdb paths
graphserverurl = 'http://localhost:7201/'
graphreponame = 'scidata'
graphuploadlocalurl = graphserverurl + 'rest/data/import/server/' + graphreponame
graphuploadremoteurl = graphserverurl + 'rest/data/upload/server/' + graphreponame + '/url/'
graphsparqlurl = graphserverurl + 'repositories/' + graphreponame
