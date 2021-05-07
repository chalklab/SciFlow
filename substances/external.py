"""functions to get metadata/identifiers/descriptors from external websites"""
import re
from qwikidata.sparql import *
from qwikidata.entity import *
from qwikidata.typedefs import *
from qwikidata.linked_data_interface import *
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
        other = identifier
        uhff = '-UHFFFAOYSA-N'
        identifier = str(re.search('^[A-Z]{14}', identifier).group(0)) + uhff
        respnse = requests.get(apipath + 'inchikey/' + identifier + '/json')
        if respnse.status_code == 200:
            notes = "InChiKey generalized with -UHFFFAOYSA-N"
            srcs["pubchem"].update({"result": 0, "notes": notes})
        else:
            notes = "InChIKey not found, including generic"
            srcs["pubchem"].update({"result": 0, "notes": notes})
            return

    # OK compound has been found go get the data
    json = requests.get(apipath + 'inchikey/' + identifier + '/json').json()
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
    if other:
        ids["pubchem"]["other"] = other  # original inchikey if made generic
    for prop in props:
        if prop['urn']['label'] == "IUPAC Name" and \
                prop['urn']['name'] == "Preferred":
            ids["pubchem"]["iupacname"] = prop["value"]["sval"]
        elif prop['urn']['label'] == "InChI":
            ids["pubchem"]["inchi"] = prop["value"]["sval"]
        elif prop['urn']['label'] == "InChIKey":
            ids["pubchem"]["inchikey"] = prop["value"]["sval"]
        elif prop['urn']['label'] == "SMILES" and \
                prop['urn']['name'] == "Canonical":
            ids["pubchem"]["csmiles"] = prop["value"]["sval"]
        elif prop['urn']['label'] == "SMILES" and \
                prop['urn']['name'] == "Isomeric":
            ids["pubchem"]["ismiles"] = prop["value"]["sval"]
        elif prop['urn']['label'] == "Molecular Formula":
            meta["pubchem"]["formula"] = prop["value"]["sval"]
        elif prop['urn']['label'] == "Molecular Weight":
            meta["pubchem"]["mw"] = prop["value"]["fval"]
        elif prop['urn']['label'] == "Weight":
            meta["pubchem"]["mim"] = prop["value"]["fval"]
        elif prop['urn']['label'] == "Count" and \
                prop['urn']['name'] == "Hydrogen Bond Acceptor":
            descs["pubchem"]["h_bond_acceptor"] = prop["value"]["ival"]
        elif prop['urn']['label'] == "Count" and \
                prop['urn']['name'] == "Hydrogen Bond Donor":
            descs["pubchem"]["h_bond_donor"] = prop["value"]["ival"]
        elif prop['urn']['label'] == "Count" and \
                prop['urn']['name'] == "Rotatable Bond":
            descs["pubchem"]["rotatable_bond"] = prop["value"]["ival"]

        # get addition descriptor data if available
        search = 'inchikey/' + identifier + '/json?record_type=3d'
        response = requests.get(apipath + search)
        if response.status_code == 200:
            search = 'inchikey/' + identifier + '/json?record_type=3d'
            json = requests.get(apipath + search).json()
            full = json["PC_Compounds"][0]
            coords = full["coords"]
            for coord in coords:
                for x in coord["conformers"]:
                    for y in x["data"]:
                        if y["urn"]["label"] == "Fingerprint" and \
                                y["urn"]["name"] == "Shape":
                            descs["pubchem"]["fingerprint"] = \
                                y["value"]["slist"]
                        elif y["urn"]["label"] == "Shape" and \
                                y["urn"]["name"] == "Volume":
                            descs["pubchem"]["volume3D"] = y["value"]["fval"]

        srcs["pubchem"].update({"result": 1})


def classyfire(identifier, descs, srcs):
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
        # redefine identifier
        uhff = '-UHFFFAOYSA-N'
        identifier = str(re.search('^[A-Z]{14}', identifier).group(0)) + uhff
        respnse = requests.get(apipath + identifier + '.json')
        if respnse.status_code == 200:
            notes = "InChiKey generalized by change to block1-UHFFFAOYSA-N"
            srcs["classyfire"].update({"result": 0, "notes": notes})

    # have we found the compound?
    if respnse.status_code != 200:
        notes = "InChIKey Not Found, including generic"
        srcs["classyfire"].update({"result": 0, "notes": notes})
        return

    # OK compound has been found go get the data
    descs["classyfire"] = {}
    respnse = requests.get(apipath + identifier + '.json').json()
    descs["classyfire"]["kingdom"] = \
        str(respnse['kingdom']["chemont_id"])
    descs["classyfire"]["superclass"] = \
        str(respnse['superclass']["chemont_id"])
    descs["classyfire"]["class"] = str(respnse['class']["chemont_id"])
    if respnse["subclass"] is not None:
        descs["classyfire"]["subclass"] = \
            str(respnse['subclass']["chemont_id"])
    if "node" in respnse.keys():
        if respnse["node"] is not None:
            descs["classyfire"]["node"] = []
            for node in respnse['intermediate_nodes']:
                descs["classyfire"]["node"].append(node["chemont_id"])
    descs["classyfire"]["direct_parent"] = \
        str(respnse['direct_parent']["chemont_id"])
    descs["classyfire"]["alternative_parent"] = []
    for alt in respnse['alternative_parents']:
        descs["classyfire"]["alternative_parent"].append(alt["chemont_id"])
    srcs["classyfire"].update({"result": 1})


w = "https://www.wikidata.org/w/api.php?action=wbgetclaims&format=json&entity="


def wikidata(identifier, ids, srcs):
    """ retreive data from wikidata using the qwikidata python package"""
    # find wikidata code for a compound based off its inchikey (wdt:P35)
    srcs.update({"wikidata": {}})

    # check identifier for inchikey pattern
    if re.search('[A-Z]{14}-[A-Z]{10}-[A-Z]', identifier) is None:
        srcs["classyfire"].update({"result": 0, "notes": "Not an InChIKey"})
        return

    # setup SPARQL query
    q1 = "SELECT DISTINCT ?compound "
    q2 = "WHERE { ?compound wdt:P235 \"" + identifier + "\" ."
    q3 = 'SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }}'
    query = q1 + q2 + q3
    res = return_sparql_query_results(query)
    if not res['results']['bindings']:
        uhff = '-UHFFFAOYSA-N'
        identifier = str(re.search('^[A-Z]{14}', identifier).group(0)) + uhff
        q2 = "WHERE { ?compound wdt:P235 \"" + identifier + "\" ."
        query = q1 + q2 + q3
        res = return_sparql_query_results(query)
        if res['results']['bindings']:
            # TODO: why was this here? request.session['originalkey']
            notes = "InChiKey generalized by change to block1-UHFFFAOYSA-N"
            srcs["wikidata"].update({"result": 0, "notes": notes})

    # have we found the compound?
    if not res['results']['bindings']:
        notes = "InChIKey not found, including generic"
        srcs["wikidata"].update({"result": 0, "notes": notes})
        return

    # OK compound has been found go get the data
    eurl = res['results']['bindings'][0]['compound']['value']
    wdid = str(eurl).replace("http://www.wikidata.org/entity/", "")
    mwurl = w + wdid  # 'w' is defined (above) outside of this function
    respnse = requests.get(mwurl)
    if respnse.status_code == 200:
        # response contains many props from which we get specific chemical ones
        ids['wikidata'] = {}
        json = requests.get(mwurl).json()
        claims = json['claims']
        propids = {'casrn': 'P231', 'atc': 'P267', 'inchi': 'P234',
                   'inchikey': 'P235', 'chemspider': 'P661', 'pubchem': 'P662',
                   'reaxys': 'P1579', 'gmelin': 'P1578', 'chebi': 'P683',
                   'chembl': 'P592', 'rtecs': 'P657', 'dsstox': 'P3117'}
        vals = list(propids.values())
        keys = list(propids.keys())
        for propid, prop in claims.items():
            if propid in vals:
                if 'datavalue' in prop[0]['mainsnak']:
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
    srcs.update({"chembl": {"result": None, "notes": None}})
    print(identifier)
    cmpds = molecule.search(identifier)
    found = {}
    for cmpd in cmpds:
        if cmpd['molecule_structures']['standard_inchi_key'] == identifier:
            found = cmpd
            break
    if not found:
        uhff = '-UHFFFAOYSA-N'
        genericid = str(re.search('^[A-Z]{14}', identifier).group(0)) + uhff
        cmpds = molecule.search(genericid)
        found = {}
        for cmpd in cmpds:
            if cmpd['molecule_structures']['standard_inchi_key'] == identifier:
                found = cmpd
                break
        if found:
            notes = "InChiKey generalized by change to block1-UHFFFAOYSA-N"
            srcs['chembl'].update({"notes": notes})

    if not found:
        return

    # general metadata
    cmpd = found
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
    if cmpd['atc_classifications']:
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
    srcs.update({"chembl": {"result": 1, "notes": None}})


def comchem(identifier, meta, ids, srcs):
    """ retreive data from the commonchemistry API"""
    srcs.update({"comchem": {}})

    # check identifier for inchikey pattern
    if re.search('[A-Z]{14}-[A-Z]{10}-[A-Z]', identifier) is None:
        srcs["comchem"].update({"result": 0, "notes": "Not a CAS-RN"})
        return

    # search for entries and retrieve casrn for compound if present
    apipath = "https://commonchemistry.cas.org/"
    respnse = requests.get(apipath + 'api/search?q=' + identifier).json()
    if respnse['count'] == 0:
        srcs["comchem"].update({"result": 0, "notes": "InChIKey not found"})
        return False
    else:
        # even though there may be multiple responses, first is likely correct
        casrn = respnse['results'][0]['rn']
        res = requests.get(apipath + 'api/detail?cas_rn=' + casrn).json()

    # OK now we have data for the specfic compound
    ids["comchem"] = {}
    ids["comchem"]["casrn"] = casrn
    ids["comchem"]["inchi"] = res["inchi"]
    ids["comchem"]["inchikey"] = res["inchiKey"]
    ids["comchem"]["csmiles"] = res["canonicalSmile"]
    ids["comchem"]["othername"] = res["synonyms"]
    ids["comchem"]["replacedcasrn"] = res["replacedRns"]

    meta["comchem"] = {}
    meta["comchem"]["formula"] = res["molecularFormula"]
    meta["comchem"]["mw"] = res["molecularMass"]

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
    url = apipath + pcid + '/SDF'
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
