"""functions to get metadata/identifiers/descriptors from external websites"""
import requests

# target_id = "CHEMBL240"

# def search_uniprot(identifier, meta, ids, descs, srcs):


def search_chembl(identifier, meta, ids, descs, srcs):
    """this function allows retrieval of data from the PugRest API @ PubChem"""
    apipath = "https://www.ebi.ac.uk/chembl/api/data/target/"
    srcs.update({"chembl": {}})

    # check to see if compound is in database
    respnse = requests.get(apipath+identifier+".json")
    if respnse.status_code != 200:
        notes = "ChemblID not found"
        srcs["chembl"].update({"result": 0, "notes": notes})
        return

    # OK compound has been found go get the data

    reqdata = requests.get(apipath+identifier+".json").json()
    target_components = reqdata['target_components']
    chembl_target_components = []
    for group in target_components:
        chembl_target_components.append({
            'accession': group['accession'],
            'component_description': group['component_description'],
            'component_id': group['component_id'],
            'component_type': group['component_type'],
            'relationship': group['relationship']
        })

    descs["chembl"] = {}
    ids["chembl"] = {}
    meta["chembl"] = {}

    ids["chembl"]["chembl_id"] = identifier
    if reqdata.get('pref_name'):
        ids["chembl"]["pref_name"] = reqdata.get('pref_name')
    if reqdata.get('organism'):
        ids["chembl"]["organism"] = reqdata.get('organism')
    if reqdata.get('target_type'):
        ids["chembl"]["target_type"] = reqdata.get('target_type')
    if reqdata.get('tax_id'):
        ids["chembl"]["tax_id"] = reqdata.get('tax_id')

    accession = []
    for com in chembl_target_components:
        if com.get('accession'):
            accession.append(com.get('accession'))
    # print(accession)

    if accession:
        ids["chembl"]["accession_id"] = accession
    # print(json.dumps(reqdata))
    return


def search_chembl2085_identifier():
    identifier = "CHEMBL2085"
    return identifier

# identifier, meta, ids, descs, srcs = "CHEMBL240", "",{},{},{}
# search_chembl(identifier, meta, ids, descs, srcs)
