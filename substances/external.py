"""functions to get metadata/identifiers/descriptors from external websites"""
import json
import re
import requests
from qwikidata.sparql import return_sparql_query_results
from qwikidata.entity import WikidataItem
from qwikidata.typedefs import ItemId
from qwikidata.linked_data_interface import get_entity_dict_from_api
from chembl_webresource_client.new_client import new_client


def pubchem(identifier, meta, ids, descs, srcs):
    """this function allows retrieval of data from the PugRest API @ PubChem"""
    apipath = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
    srcs.update({"pubchem": {}})

    # check identifier for inchikey pattern
    if re.search('[A-Z]{14}-[A-Z]{10}-[A-Z]', identifier) is None:
        srcs["pubchem"].update({"result": 0, "notes": "Not an InChIKey"})
        return

    # check to see if compound is in database
    other = None
    respnse = requests.get(apipath + 'inchikey/' + identifier + '/json')
    if respnse.status_code != 200:
        notes = "InChIKey  " + identifier + " not found"
        srcs["pubchem"].update({"result": 0, "notes": notes})
        return

    # OK compound has been found go get the data
    jsn = requests.get(apipath + 'inchikey/' + identifier + '/json').json()
    full = jsn["PC_Compounds"][0]
    pcid = full["id"]["id"]["cid"]
    props = full["props"]
    counts = dict(full["count"])
    descs["pubchem"] = {}
    for k, v in counts.items():
        descs["pubchem"][k] = v

    ids["pubchem"] = {}
    meta["pubchem"] = {}
    ids["pubchem"]["pubchem"] = pcid
    if other:
        ids["pubchem"]["othername"] = other  # original inchikey if made generic
    for prop in props:
        # 'name' not added to meta as common name not available in CID download
        # iupacname in meta used as a check for entry in DB
        if prop['urn']['label'] == "IUPAC Name" and prop['urn']['name'] == "Preferred":
            ids["pubchem"]["iupacname"] = prop["value"]["sval"]
            meta["pubchem"]["iupacname"] = prop["value"]["sval"]
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
            meta["pubchem"]["mw"] = prop["value"]["sval"]
        elif prop['urn']['label'] == "Weight":
            meta["pubchem"]["mim"] = prop["value"]["sval"]
        elif prop['urn']['label'] == "Count" and prop['urn']['name'] == "Hydrogen Bond Acceptor":
            descs["pubchem"]["h_bond_acceptor"] = prop["value"]["ival"]
        elif prop['urn']['label'] == "Count" and prop['urn']['name'] == "Hydrogen Bond Donor":
            descs["pubchem"]["h_bond_donor"] = prop["value"]["ival"]
        elif prop['urn']['label'] == "Count" and prop['urn']['name'] == "Rotatable Bond":
            descs["pubchem"]["rotatable_bond"] = prop["value"]["ival"]
        srcs["pubchem"].update({"result": 1})


def classyfire(identifier, ids, descs, srcs):
    """ get classyfire classification for a specific compound """
    # best to use InChIKey to get the data
    apipath = "http://classyfire.wishartlab.com/entities/"
    srcs.update({"classyfire": {}})

    # check identifier for inchikey pattern
    if re.search('[A-Z]{14}-[A-Z]{10}-[A-Z]', identifier) is None:
        srcs["classyfire"].update({"result": 0, "notes": "Not an InChIKey"})
        return

    # check to see if compound is in database
    respnse = requests.get(apipath + identifier + '.json')
    if respnse.status_code != 200:
        notes = "InChIKey  " + identifier + " not found"
        srcs["classyfire"].update({"result": 0, "notes": notes})
        return

    # OK compound has been found go get the data
    ids["classyfire"] = {}
    descs["classyfire"] = {}
    respnse = requests.get(apipath + identifier + '.json').json()

    if 'inchikey' not in respnse.keys():
        # not in classyfire
        notes = "Compound not classified"
        srcs["classyfire"].update({"result": 0, "notes": notes})
        return
    else:
        ids["classyfire"]['inchikey'] = str(respnse['inchikey']).replace("InChIKey=", "")

    if 'smiles' in respnse.keys():
        ids["classyfire"]['csmiles'] = str(respnse['smiles'])

    if 'kingdom' in respnse.keys() and respnse['kingdom'] is not None:
        descs["classyfire"]["kingdom"] = str(respnse['kingdom']["chemont_id"])
    if 'superclass' in respnse.keys() and respnse['superclass'] is not None:
        descs["classyfire"]["superclass"] = str(respnse['superclass']["chemont_id"])
    if 'class' in respnse.keys() and respnse['class'] is not None:
        descs["classyfire"]["class"] = str(respnse['class']["chemont_id"])
    if 'subclass' in respnse.keys() and respnse['subclass'] is not None:
        descs["classyfire"]["subclass"] = str(respnse['subclass']["chemont_id"])
    if 'intermediate_nodes' in respnse.keys():
        descs["classyfire"]["node"] = []
        for node in respnse['intermediate_nodes']:
            descs["classyfire"]["node"].append(node["chemont_id"])
    if 'direct_parent' in respnse.keys() and respnse['direct_parent'] is not None:
        descs["classyfire"]["direct_parent"] = str(respnse['direct_parent']["chemont_id"])
    if 'alternative_parents' in respnse.keys():
        descs["classyfire"]["alternative_parent"] = []
        for alt in respnse['alternative_parents']:
            descs["classyfire"]["alternative_parent"].append(alt["chemont_id"])
    srcs["classyfire"].update({"result": 1})


def wikidata(identifier, ids, srcs):
    """ retreive data from wikidata using the qwikidata python package"""
    # find wikidata code for a compound based off its inchikey (wdt:P35)
    srcs.update({"wikidata": {}})
    w = "https://www.wikidata.org/w/api.php?action=wbgetclaims&format=json&entity="

    # check identifier for inchikey pattern
    if re.search('[A-Z]{14}-[A-Z]{10}-[A-Z]', identifier) is None:
        srcs["wikidata"].update({"result": 0, "notes": "Not an InChIKey"})
        return

    # setup SPARQL query
    q1 = "SELECT DISTINCT ?compound "
    q2 = "WHERE { ?compound wdt:P235 \"" + identifier + "\" ."
    q3 = 'SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }}'
    query = q1 + q2 + q3
    res = return_sparql_query_results(query)
    if 'bindings' in res['results'].keys() and not res['results']['bindings']:
        notes = "InChIKey  " + identifier + " not found"
        srcs["wikidata"].update({"result": 0, "notes": notes})
        return

    # OK compound has been found go get the data
    eurl = res['results']['bindings'][0]['compound']['value']
    wdid = str(eurl).replace("http://www.wikidata.org/entity/", "")  # keep no SSL
    mwurl = w + wdid  # 'w' is defined (above)
    respnse = requests.get(mwurl)
    if respnse.status_code == 200:
        # response contains many props from which we get specific chemical ones
        ids['wikidata'] = {}
        jsn = None
        try:
            jsn = requests.get(mwurl).json()
        except ValueError:
            # https://stackoverflow.com/questions/8381193/handle-json-decode-error-when-nothing-returned
            print('JSONDecodeError!')
            print(mwurl)
            exit()
        claims = jsn['claims']
        propids = {'casrn': 'P231', 'atc': 'P267', 'inchi': 'P234', 'inchikey': 'P235', 'chemspider': 'P661',
                   'pubchem': 'P662', 'reaxys': 'P1579', 'gmelin': 'P1578', 'chebi': 'P683', 'chembl': 'P592',
                   'rtecs': 'P657', 'dsstox': 'P3117', 'unii': 'P562', 'drugbank': 'P715', 'csmiles': 'P233',
                   'ismiles': 'P2017', 'mlights': 'P3890', 'mesh': 'P6680', 'massbank': 'P6689', 'ccdc': 'P6852'}
        vals = list(propids.values())
        keys = list(propids.keys())
        for propid, prop in claims.items():
            if propid in vals:
                if 'datavalue' in prop[0]['mainsnak'].keys():
                    value = prop[0]['mainsnak']['datavalue']['value']
                    key = keys[vals.index(propid)]
                    ids['wikidata'].update({key: value})

        # get aggregated names/tradenames for this compound (and intl names)
        cdict = get_entity_dict_from_api(ItemId(wdid))
        cmpd = WikidataItem(cdict)
        ids['wikidata']['othername'] = []
        aliases = cmpd.get_aliases()
        aliases = list(set(aliases))  # deduplicate
        for alias in aliases:
            ids['wikidata']['othername'].append(alias)
        ids['wikidata']['othername'] = list(set(ids['wikidata']['othername']))
        srcs["wikidata"].update({"result": 1})
    else:
        notes = "Could not get Wikidata entity '" + wdid + "'"
        srcs["wikidata"].update({"result": 0, "notes": notes})


def chembl(identifier, meta, ids, descs, srcs):
    """ retrieve data from the ChEMBL repository"""
    molecule = new_client.molecule
    srcs.update({"chembl": {}})
    found = molecule.filter(molecule_structures__standard_inchi_key=identifier)
    notes = None
    result = 0
    if not found:
        notes = "InChiKey " + identifier + " not found"
        srcs["chembl"].update({"result": 0, "notes": notes})
        return

    cmpd = found[0]

    # general metadata
    meta['chembl'] = {}
    mprops = ['full_molformula', 'full_mwt', 'mw_freebase', 'mw_monoisotopic']
    for k, v in cmpd['molecule_properties'].items():
        if k in mprops:
            meta['chembl'].update({k: v})
    meta['chembl'].update({'prefname': cmpd['pref_name']})

    # identifiers
    ids['chembl'] = {}
    # molecule structures ('canonical smiles' is actually
    # 'isomeric canonical smiles')
    exclude = ['molfile']
    rename = {'canonical_smiles': 'ismiles', 'standard_inchi': 'inchi',
              'standard_inchi_key': 'inchikey'}
    for k, v in cmpd['molecule_structures'].items():
        if k not in exclude:
            ids['chembl'].update({rename[k]: v})
    # - molecule synonyms
    syntypes = []
    for syn in cmpd['molecule_synonyms']:
        syntype = syn['syn_type'].lower()
        syntypes.append(syntype)
        if syntype not in ids['chembl'].keys():
            ids['chembl'][syntype] = []
        ids['chembl'][syntype].append(syn['molecule_synonym'])
    #   deduplicate entries for synonym types
    syntypes = set(list(syntypes))
    for syntype in syntypes:
        ids['chembl'][syntype] = list(set(ids['chembl'][syntype]))
    # descriptors
    descs['chembl'] = {}
    # - atc
    if 'atc_classifications' in cmpd.keys():
        descs['chembl'].update(atclvl1=[], atclvl2=[],
                               atclvl3=[], atclvl4=[], atclvl5=[])
        for c in cmpd['atc_classifications']:
            descs['chembl']['atclvl1'].append(c[0:1])
            descs['chembl']['atclvl2'].append(c[0:3])
            descs['chembl']['atclvl3'].append(c[0:4])
            descs['chembl']['atclvl4'].append(c[0:5])
            descs['chembl']['atclvl5'].append(c)
        descs['chembl']['atclvl1'] = list(set(descs['chembl']['atclvl1']))
        descs['chembl']['atclvl2'] = list(set(descs['chembl']['atclvl2']))
        descs['chembl']['atclvl3'] = list(set(descs['chembl']['atclvl3']))
        descs['chembl']['atclvl4'] = list(set(descs['chembl']['atclvl4']))
        descs['chembl']['atclvl5'] = list(set(descs['chembl']['atclvl5']))
    # - molecule properties
    for k, v in cmpd['molecule_properties'].items():
        if k not in mprops:
            if v is not None:
                descs['chembl'].update({k: v})
    # - other fields
    dflds = ['chirality', 'dosed_ingredient', 'indication_class',
             'inorganic_flag', 'max_phase', 'molecule_type', 'natural_product',
             'polymer_flag', 'structure_type', 'therapeutic_flag']
    for fld in dflds:
        if cmpd[fld] is not None:
            descs['chembl'].update({fld: cmpd[fld]})

    # sources
    srcs.update({"chembl": {"result": 1}})


def comchem(identifier, meta, ids, srcs):
    """ retrieve data from the commonchemistry API"""
    srcs.update({"comchem": {}})

    # check identifier for inchikey pattern
    if re.search('[A-Z]{14}-[A-Z]{10}-[A-Z]', identifier) is None:
        srcs["comchem"].update({"result": 0, "notes": "Not a CAS-RN"})
        return False

    # search for entries and retrieve casrn for compound if present
    apipath = "https://commonchemistry.cas.org/"
    respnse = requests.get(apipath + 'api/search?q=InChIKey=' + identifier).json()
    if respnse['count'] == 0:
        notes = "InChIKey " + identifier + " not found"
        srcs["comchem"].update({"result": 0, "notes": notes})
        return False

    # even though there may be multiple responses, first is likely correct
    casrn = respnse['results'][0]['rn']
    res = requests.get(apipath + 'api/detail?cas_rn=' + casrn).json()

    # OK now we have data for the specfic compound
    ids["comchem"] = {}
    ids["comchem"]["casrn"] = casrn
    ids["comchem"]["inchi"] = res["inchi"]
    ids["comchem"]["inchikey"] = res["inchiKey"].replace('InChIKey=', '')
    ids["comchem"]["csmiles"] = res["canonicalSmile"]
    ids["comchem"]["othername"] = res["synonyms"]
    ids["comchem"]["replacedcasrn"] = res["replacedRns"]

    meta["comchem"] = {}
    meta["comchem"]["name"] = res["name"]
    meta["comchem"]["formula"] = res["molecularFormula"].replace('<sub>', '').replace('</sub>', '')
    meta["comchem"]["mw"] = res["molecularMass"]
    meta["comchem"]["casrn"] = casrn

    srcs["comchem"].update({"result": 1})
    return True


def pubchemsyns(identifier):
    """this function allows retreival of data from the PugRest API @ PubChem"""
    apipath = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"

    # retrieve full record if available based on name
    searchpath = 'name/' + identifier + '/synonyms/json'
    response = requests.get(apipath + searchpath).json()
    syns = response["InformationList"]["Information"][0]["Synonym"]
    inchikey = ""
    for k in syns:
        m = re.search('^[A-Z]{14}-[A-Z]{10}-[A-Z]$', k)
        if m:
            inchikey = k

    return inchikey


def pubchemmol(pcid):
    """
    allows retrieval of SDF file from the PugRest API at PubChem
        with two entries - atoms and bonds.  Each value is a list
                atoms list is x, y, z coords and element symbol
                bonds list is atom1, atom2, and bond order
    :param pcid pubchem id for compound
    :return dict dictionary
    """
    apipath = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"
    url = apipath + str(pcid) + '/SDF'
    response = requests.get(url)
    sdf = None
    if response.status_code == 200:
        sdf = requests.get(url).text

    atoms = []
    bonds = []
    chrgs = []
    for ln in sdf.splitlines():
        a = re.search(r"([0-9\-.]+)\s+([0-9\-.]+)\s+([0-9\-.]+)\s"
                      r"([A-Za-z]{1,2})\s+0\s+(\d)\s+0\s+0", ln)
        if a:
            atoms.append([a[1], a[2], a[3], a[4], a[5]])
            continue
        b = re.search(r"^\s+(\d{1,2})\s+(\d{1,2})\s+(\d)\s+0\s+0\s+0\s+0$", ln)
        if b:
            bonds.append([b[1], b[2], b[3]])
            continue
        c = re.search(r"^M\s+CHG\s+(\d)", ln)
        if c:
            num = int(c[1])
            rest = ln.replace('M  CHG  ' + str(num), '')
            parts = re.split(r"\s{2,3}", rest.strip())
            for idx, val in enumerate(parts):
                if (idx % 2) != 0:
                    continue
                chrgs.append([val, parts[(idx + 1)]])

    return {'atoms': atoms, 'bonds': bonds, 'chrgs': chrgs}
