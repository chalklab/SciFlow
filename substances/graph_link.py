import json
from sciflow.wsgi import *
from substances.functions import *
from substances.models import Substances
from substances.models import Identifiers

url = "https://stuchalk.github.io/scidata/examples/cif/1000118.jsonld"

"Post jsonld at url to graph"
def Post(test):
    headers = {'Content-Type': 'application/json',
        'Accept': 'application/json'}
    x = '"{}"'.format(test)
    data = '{\n   "data": '+x+' \n }'
    requests.post('http://localhost:7200/rest/data/import/upload/Test/url', headers=headers, data=data)
# Post(url)

cifs = '/Users/n01448636/Documents/Google Drive/CIF_scidata_jsonlds/'
directory = os.fsencode(cifs)

def GraphLinkA(file):
    jsonfile = json.load(file)
    try:
        for group in jsonfile['@graph']['scidata']['system']['facets']:
            if group['@id'].startswith(('compound/', 'crystal/')):
                newgroup = GraphLinkB(group)
                group.clear()
                group.update(newgroup)
    except:
        pass
    return jsonfile

def GraphLinkB(group):
    group = {'@id': 'compound/1/', '@type': 'cif:compound', '_chemical_formula_moiety': 'C12 H8',
            '_chemical_name_systematic': 'Q194207'}
    tablematch = {"compound":[Identifiers,Substances,'substance_id'], "crystal":[Identifiers,Substances,'substance_id']}
    identifier = {'@id': group['@id']}
    category = group['@id'].split('/')[0]
    for line in list(tablematch[category][0].objects.values()):
        try:
            if any(line['value'] in q for q in group.values()):
                if line['value'] in group.values():
                    group = identifier
                    group.update(tablematch[category][1].objects.values('graphdb').get(id=line[tablematch[category][2]]))
                    # Post(y)
            else:
                # compound/crystal/etc not found in database. Needs to be added first in order to link
                # then GraphLinkB(group)
                pass
        except:
            print('exception')
    return group


for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename == 'ACENYL.jsonld':
        xfile = directory.decode("utf-8") + filename
        with open(xfile) as x:
            output = GraphLinkA(x)
            temp = json.dumps(output, indent=4, ensure_ascii=False)
            print(temp)