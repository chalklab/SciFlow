""" functions to get metdata, identifiers, and descriptors from external websites"""
import re
from qwikidata.sparql import *
from qwikidata.entity import *
from qwikidata.linked_data_interface import *


def pubchem(identifier, meta, ids, descs):
    """ this definition allows retreival of data from the PugRest API at PubChem"""
    apipath = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"

    # retrieve full record if available based on name
    response = requests.get(apipath + 'name/' + identifier + '/json').json()
    full = response["PC_Compounds"][0]
    props = full["props"]
    counts = dict(full["count"])
    descs["pubchem"] = {}
    for k, v in counts.items():
        descs["pubchem"][k] = v

    ids["pubchem"] = {}
    meta["pubchem"] = {}
    for prop in props:
        if prop['urn']['label'] == "IUPAC Name" and prop['urn']['name'] == "Preferred":
            ids["pubchem"]["iupacname"] = prop["value"]["sval"]
        elif prop['urn']['label'] == "InChI":
            ids["pubchem"]["inchi"] = prop["value"]["sval"]
        elif prop['urn']['label'] == "InChIKey":
            ids["pubchem"]["inchikey"] = prop["value"]["sval"]
        elif prop['urn']['label'] == "SMILES" and prop['urn']['name'] == "Canonical":
            ids["pubchem"]["csmiles"] = prop["value"]["sval"]
        elif prop['urn']['label'] == "SMILES" and prop['urn']['name'] == "Isomeric":
            ids["pubchem"]["ismiles"] = prop["value"]["sval"]
        elif prop['urn']['label'] == "Molecular Formula":
            meta["pubchem"]["formula"] = prop["value"]["sval"]
        elif prop['urn']['label'] == "Molecular Weight":
            meta["pubchem"]["mw"] = prop["value"]["fval"]
        elif prop['urn']['label'] == "Weight":
            meta["pubchem"]["mim"] = prop["value"]["fval"]
        elif prop['urn']['label'] == "Count" and prop['urn']['name'] == "Hydrogen Bond Acceptor":
            descs["pubchem"]["h_bond_acceptor"] = prop["value"]["ival"]
        elif prop['urn']['label'] == "Count" and prop['urn']['name'] == "Hydrogen Bond Donor":
            descs["pubchem"]["h_bond_donor"] = prop["value"]["ival"]
        elif prop['urn']['label'] == "Count" and prop['urn']['name'] == "Rotatable Bond":
            descs["pubchem"]["rotatable_bond"] = prop["value"]["ival"]

    return meta, ids, descs


def classyfire(identifier, meta, ids, descs):
    """ get classyfire classification for a specific compound """
    # best to use InChIKey to get the data
    apipath = "http://classyfire.wishartlab.com/entities/"

    # check identifier for inchikey pattern
    m = re.search('[A-Z]{14}-[A-Z]{10}-[A-Z]', identifier)

    if m:
        response = requests.get(apipath + identifier + '.json')
        if response.status_code == 200:
            descs["classyfire"] = {}
            response = requests.get(apipath + identifier + '.json').json()
            descs["classyfire"]["kingdom"] = str(response['kingdom']["chemont_id"])
            descs["classyfire"]["superclass"] = str(response['superclass']["chemont_id"])
            descs["classyfire"]["class"] = str(response['class']["chemont_id"])
            descs["classyfire"]["subclass"] = str(response['subclass']["chemont_id"])
            count = 1
            for node in response['intermediate_nodes']:
                descs["classyfire"]["node" + str(count)] = node["chemont_id"]
                count += 1
            descs["classyfire"]["direct_parent"] = str(response['direct_parent']["chemont_id"])
            count = 1
            for node in response['alternative_parents']:
                descs["classyfire"]["alt_parent" + str(count)] = node["chemont_id"]
                count += 1
        else:
            print('Invalid InChIKey')
            return

    else:
        print("Invalid InChIKey")

    return meta, ids, descs


def wikidata(identifier, meta, ids, descs):
    """ retreive data from wikidata using the qwikidata python package"""
    # find wikidata code for a compound based off its inchikey
    query1 = "SELECT DISTINCT ?compound "
    query2 = "WHERE { ?compound wdt:P235 \"" + identifier + "\" ."
    query3 = "SERVICE wikibase:label { bd:serviceParam wikibase:language \"en\". } }"
    query = query1 + query2 + query3
    res = return_sparql_query_results(query)

    # TODO add code to get the name of a compound in each language...

    # now get all data associated with this wikidata entry
    # create an item representing "Douglas Adams"
    url = res['results']['bindings'][0]['compound']['value']
    wdid = str(url).replace("http://www.wikidata.org/entity/", "")

    mwurl = "https://www.wikidata.org/w/api.php?action=wbgetclaims&format=json&entity=" + wdid
    response = requests.get(mwurl).json()
    # response contains many properties from which we need to grab specific chemical ones...
    ids['wikidata'] = {}
    claims = response['claims']
    propids = {'casrn': 'P231', 'atc': 'P267', 'inchi': 'P234', 'inchikey': 'P235', 'chemspiderid': 'P661',
               'pubchemid': 'P662', 'reaxys': 'P1579', 'gmelin': 'P1578', 'chebi': 'P683', 'chembl': 'P592',
               'rtecs': 'P657', 'dsstox': 'P3117'}
    vals = list(propids.values())
    keys = list(propids.keys())
    for propid, prop in claims.items():
        if propid in vals:
            if 'datavalue' in prop[0]['mainsnak']:
                value = prop[0]['mainsnak']['datavalue']['value']
                key = keys[vals.index(propid)]
                ids['wikidata'].update({key: value})

    # get aggregated names/tradenames for this compound
    cdict = get_entity_dict_from_api(wdid)
    cmpd = WikidataItem(cdict)

    count = 1
    names = cmpd.get_aliases()
    for name in names:
        ids['wikidata']['name' + str(count)] = name
        count += 1

    return meta, ids, descs


def pubchemsyns(identifier):
    """ this definition allows retreival of data from the PugRest API at PubChem"""
    apipath = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"

    # retrieve full record if available based on name
    response = requests.get(apipath + 'name/' + identifier + '/synonyms/json').json()
    syns = response["InformationList"]["Information"][0]["Synonym"]
    inchikey = ""
    for k in syns:
        m = re.search('[A-Z]{14}-[A-Z]{10}-[A-Z]', k)
        if m:
            inchikey = k

    return inchikey
