""" functions to get metadata, identifiers, and descriptors from external websites"""
import re
from qwikidata.sparql import *
from qwikidata.entity import *
from qwikidata.linked_data_interface import *
from chembl_webresource_client.new_client import new_client


def pubchem(identifier, meta, ids, descs, srcs):
    """ this definition allows retrieval of data from the PugRest API at PubChem"""
    apipath = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
    # retrieve full record if available based on name
    srcs.update({"pubchem": {"result": None, "notes": None}})
    try:
        url = apipath + 'inchikey/' + identifier + '/json'
        response = requests.get(url)
    except:
        genericinchi = str(re.search('^[A-Z]{14}', identifier).group(0)) + '-UHFFFAOYSA-N'
        url = apipath + 'inchikey/' + genericinchi + '/json'
        response = requests.get(url)
        srcs["pubchem"].update({"notes": "InChiKey generalized by substituting second and third block with -UHFFFAOYSA-N"})

    if response.status_code == 200:
        json = requests.get(url).json()
        full = json["PC_Compounds"][0]
        pcid = full["id"]["id"]["cid"]
        props = full["props"]
        counts = dict(full["count"])
        descs["pubchem"] = {}
        for k, v in counts.items():
            descs["pubchem"][k] = v

        ids["pubchem"] = {}
        meta["pubchem"] = {}
        ids["pubchem"]["pubchem"] = pcid
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

            srcs["pubchem"].update({"result": 1})

        try:
            url = apipath + 'inchikey/' + identifier + '/json?record_type=3d'
            response = requests.get(url)
            if response.status_code == 200:
                json = requests.get(url).json()
                full = json["PC_Compounds"][0]
                coords = full["coords"]
                for coord in coords:
                    for x in coord["conformers"]:
                        for y in x["data"]:
                            if y["urn"]["label"] == "Fingerprint" and y["urn"]["name"] == "Shape":
                                descs["pubchem"]["fingerprint"] = y["value"]["slist"]
                            elif y["urn"]["label"] == "Shape" and y["urn"]["name"] == "Volume":
                                descs["pubchem"]["volume3D"] = y["value"]["fval"]
        except:
            pass
    else:
        srcs["pubchem"].update({"result": 0, "notes": "InChIKey not found on PubChem"})
    return


def classyfire(identifier, meta, ids, descs, srcs):
    """ get classyfire classification for a specific compound """
    # best to use InChIKey to get the data
    apipath = "http://classyfire.wishartlab.com/entities/"

    # check identifier for inchikey pattern
    try:
        m = re.search('[A-Z]{14}-[A-Z]{10}-[A-Z]', identifier)
        srcs.update({"classyfire": {"result": None, "notes": None}})
    except:
        m = str(re.search('^[A-Z]{14}', identifier).group(0)) + '-UHFFFAOYSA-N'
        srcs.update({"classyfire": {"result": None, "notes": "InChiKey generalized by substituting second and third block with -UHFFFAOYSA-N"}})

    if m:
        response = requests.get(apipath + identifier + '.json')
        if response.status_code == 200:
            descs["classyfire"] = {}
            response = requests.get(apipath + identifier + '.json').json()
            descs["classyfire"]["kingdom"] = str(response['kingdom']["chemont_id"])
            descs["classyfire"]["superclass"] = str(response['superclass']["chemont_id"])
            descs["classyfire"]["class"] = str(response['class']["chemont_id"])
            if response["subclass"] is not None:
                descs["classyfire"]["subclass"] = str(response['subclass']["chemont_id"])
            if "node" in response.keys():
                if response["node"] is not None:
                    descs["classyfire"]["node"] = []
                    for node in response['intermediate_nodes']:
                        descs["classyfire"]["node"].append(node["chemont_id"])
            descs["classyfire"]["direct_parent"] = str(response['direct_parent']["chemont_id"])
            descs["classyfire"]["alternative_parent"] = []
            for alt in response['alternative_parents']:
                descs["classyfire"]["alternative_parent"].append(alt["chemont_id"])
            srcs["classyfire"].update({"result": 1})

        else:
            srcs["classyfire"].update({"result": 0, "notes": "InChIKey Not Found"})
    else:
        srcs["classyfire"].update({"result": 0, "notes": "Invalid InChIKey"})
    return


def wikidata(identifier, meta, ids, descs, srcs):
    """ retreive data from wikidata using the qwikidata python package"""
    # find wikidata code for a compound based off its inchikey (wdt:P35)
    query1 = "SELECT DISTINCT ?compound "
    try:
        query2 = "WHERE { ?compound wdt:P235 \"" + identifier + "\" ."
        srcs.update({"wikidata": {"result": None, "notes": None}})
    except:
        genericidentifier = str(re.search('^[A-Z]{14}', identifier).group(0)) + '-UHFFFAOYSA-N'
        query2 = "WHERE { ?compound wdt:P235 \"" + genericidentifier + "\" ."
        srcs.update({"wikidata": {"result": None, "notes": "InChiKey generalized by substituting second and third block with -UHFFFAOYSA-N"}})

    query3 = "SERVICE wikibase:label { bd:serviceParam wikibase:language \"en\". } }"
    query = query1 + query2 + query3
    res = return_sparql_query_results(query)
    srcs.update({"wikidata": {"result": None, "notes": None}})
    # TODO add code to get the name of a compound in each language...

    # now get all data associated with this wikidata entry
    try:
        url = res['results']['bindings'][0]['compound']['value']
        try:
            wdid = str(url).replace("http://www.wikidata.org/entity/", "")

            mwurl = "https://www.wikidata.org/w/api.php?action=wbgetclaims&format=json&entity=" + wdid
            response = requests.get(mwurl)
            if response.status_code == 200:
                # response contains many properties from which we need to grab specific chemical ones...
                ids['wikidata'] = {}
                json = requests.get(mwurl).json()
                claims = json['claims']
                propids = {'casrn': 'P231', 'atc': 'P267', 'inchi': 'P234', 'inchikey': 'P235', 'chemspider': 'P661',
                           'pubchem': 'P662', 'reaxys': 'P1579', 'gmelin': 'P1578', 'chebi': 'P683', 'chembl': 'P592',
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
                ids['wikidata']['othername'] = []
                aliases = cmpd.get_aliases()
                aliases = list(set(aliases))  # deduplicate
                for alias in aliases:
                    ids['wikidata']['othername'].append(alias)
                ids['wikidata']['othername'] = list(set(ids['wikidata']['othername']))
                srcs["wikidata"] = {"result": 1}

            else:
                srcs["wikidata"].update({"result": 0, "notes": "Invalid InChIKey"})
        except Exception as exception:
            srcs["wikidata"].update({"result": 0, "notes": exception})

    except Exception as exception:
        srcs["wikidata"].update({"result": 0, "notes": "Error in 'url = res['results']['bindings'][0]['compound']["
                                                       "'value']', Full exception: " + str('exception')})

    return


def chembl(identifier, meta, ids, descs, srcs):
    """ retrieve data from the ChEMBL repository"""
    molecule = new_client.molecule
    srcs.update({"chembl": {"result": None, "notes": None}})
    try:
        cmpd = molecule.search(identifier)[0]
    except:
        genericidentifier = str(re.search('^[A-Z]{14}', identifier).group(0)) + '-UHFFFAOYSA-N'
        cmpd = molecule.search(genericidentifier)[0]
        srcs['chembl'].update({"notes": "InChiKey generalized by substituting second and third block with -UHFFFAOYSA-N"})

    # general metadata
    meta['chembl'] = {}
    mprops = ['full_molformula', 'full_mwt', 'mw_freebase', 'mw_monoisotopic']
    for k, v in cmpd['molecule_properties'].items():
        if k in mprops:
            meta['chembl'].update({k: v})

    # identifiers
    ids['chembl'] = {}
    # - molecule structures ('canonical smiles' is actually 'isomeric canonical smiles'
    exclude = ['molfile']
    rename = {'canonical_smiles': 'ismiles', 'standard_inchi': 'inchi', 'standard_inchi_key': 'inchikey'}
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
    if cmpd['atc_classifications']:
        descs['chembl'].update(atclvl1=[], atclvl2=[], atclvl3=[], atclvl4=[], atclvl5=[])
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
    dflds = ['chirality', 'dosed_ingredient', 'indication_class', 'inorganic_flag', 'max_phase', 'molecule_type',
             'natural_product', 'polymer_flag', 'structure_type', 'therapeutic_flag']
    for fld in dflds:
        if cmpd[fld] is not None:
            descs['chembl'].update({fld: cmpd[fld]})

    # sources
    srcs.update({"chembl": {"result": 1, "notes": None}})


def pubchemsyns(identifier):
    """ this definition allows retreival of data from the PugRest API at PubChem"""
    apipath = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"

    # retrieve full record if available based on name
    response = requests.get(apipath + 'name/' + identifier + '/synonyms/json').json()
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
    url = apipath + pcid + '/SDF'
    response = requests.get(url)
    if response.status_code == 200:
        sdf = requests.get(url).text

    atoms = []
    bonds = []
    for line in sdf.splitlines():
        a = re.search(r"([0-9\-\.]+)\s+([0-9\-\.]+)\s+([0-9\-\.]+)\s([A-Za-z]{1,2})\s+0\s+0\s+0\s+0", line)
        if a:
            lst = [a[1], a[2], a[3], a[4]]
            atoms.append(lst)
        b = re.search(r"^\s+(\d{1,2})\s+(\d{1,2})\s+(\d)\s+0\s+0\s+0\s+0$", line)
        if b:
            lst = [b[1], b[2], b[3]]
            bonds.append(lst)

    return {'atoms': atoms, 'bonds': bonds}

pubchem('XLYOFNOQVPJJNP-UHFFFAOYSA-N', {}, {}, {}, {})