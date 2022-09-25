"""functions to get metadata/identifiers/descriptors from external websites"""
import requests
import json

# def search_uniprot(identifier, meta, ids, descs, srcs): TODO
# def search_wikidata(identifier, meta, ids, descs, srcs): TODO


# example target: identifier = "CHEMBL240"
def search_chembl(identifier, meta, ids, descs, srcs):
    """this function allows retrieval of data from the PugRest API @ PubChem"""
    apipath = "https://www.ebi.ac.uk/chembl/api/data/target/"
    srcs.update({"chembl": {}})

    # check to see if compound is in database
    respnse = requests.get(apipath + identifier + ".json")
    if respnse.status_code != 200:
        notes = "ChemblID not found"
        srcs["chembl"].update({"result": 0, "notes": notes})
        return

    # OK target has been found go get the data
    reqdata = requests.get(apipath + identifier + ".json").json()
    target_components = reqdata['target_components']
    chembl_target_components = []
    chembl_target_component_synonyms = []
    chembl_target_component_xrefs = []
    for group in target_components:
        chembl_target_components.append({
            'accession': group['accession'],
            'component_description': group['component_description'],
            'component_id': group['component_id'],
            'component_type': group['component_type'],
            'relationship': group['relationship']
        })
        chembl_target_component_synonyms.extend(group['target_component_synonyms'])
        chembl_target_component_xrefs.extend(group['target_component_xrefs'])
    descs.update({"chembl": {}})
    ids.update({"chembl": {}})
    meta.update({"chembl": {}})

    ids["chembl"].update({"chembl": identifier})
    if reqdata['pref_name']:
        ids["chembl"].update({"prefname": reqdata['pref_name']})
        meta["chembl"].update({"prefname": reqdata['pref_name']})
    if reqdata['organism']:
        meta["chembl"].update({"organism": reqdata['organism']})
    if reqdata['target_chembl_id']:
        meta["chembl"].update({"chemblid": reqdata['target_chembl_id']})
    if reqdata['target_type']:
        meta["chembl"].update({"targettype": reqdata['target_type'].lower()})
    if reqdata['tax_id']:
        meta["chembl"].update({"taxid": reqdata['tax_id']})
        ids["chembl"].update({"taxid": reqdata['tax_id']})

    accession = []
    for com in chembl_target_components:
        if com.get('accession'):
            accession.append(com.get('accession'))
    ids["chembl"]["accession_id"] = accession

    # more ids
    for nym in iter(chembl_target_component_synonyms):
        syntype = nym['syn_type'].lower()
        if syntype not in ids["chembl"]:
            ids["chembl"][syntype] = []
        ids["chembl"][syntype].append(nym['component_synonym'])
    if reqdata['cross_references']:
        for crossref in reqdata['cross_references']:
            ids["chembl"].update({crossref['xref_src'].lower(): [crossref['xref_id']]})
    for xref in chembl_target_component_xrefs:
        reftype = xref['xref_src_db'].lower()
        if not reftype.startswith('go'):
            if reftype not in ids["chembl"]:
                ids["chembl"][reftype] = []
            ids["chembl"][reftype].append(xref['xref_id'])

    # descriptors
    for xref in chembl_target_component_xrefs:
        reftype = xref['xref_src_db'].lower()
        if reftype.startswith('go'):
            if reftype not in descs["chembl"]:
                descs["chembl"][reftype] = []
            descs["chembl"][reftype].append(xref['xref_id'])

    return


def search_chembl2085_identifier():
    identifier = "CHEMBL2085"
    return identifier

# identifier, meta, ids, descs, srcs = "CHEMBL240", "",{},{},{}
# search_chembl(identifier, meta, ids, descs, srcs)
