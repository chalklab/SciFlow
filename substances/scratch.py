""" scratch file """
from chembl_webresource_client.new_client import new_client
from substances.sources import chembl
import json


def test(identifier):
    """ searches for compound in database and gets its data or adds new compound with data"""
    meta, ids, descs = {}, {}, {}
    molecule = new_client.molecule
    response = molecule.search(identifier)
    cmpd = response[0]
    # general metadata
    meta['chembl'] = {}
    mprops = ['full_molformula', 'full_mwt', 'mw_freebase', 'mw_monoisotopic']
    for k, v in cmpd['molecule_properties'].items():
        if k in mprops:
            meta['chembl'].update({k: v})
    print(meta)
    # identifiers
    ids['chembl'] = {}
    # - molecule structures ('canonical smiles' is actually 'isomeric canonical smiles'
    exclude = ['molfile']
    for k, v in cmpd['molecule_structures'].items():
        if k not in exclude:
            ids['chembl'].update({k: v})
    # - molecule synonyms
    for syn in cmpd['molecule_synonyms']:
        syntype = syn['syn_type'].lower()
        if syntype not in ids['chembl'].keys():
            ids['chembl'][syntype] = []
        ids['chembl'][syntype].append(syn['molecule_synonym'])
    print(ids)
    # descriptors
    descs['chembl'] = {}
    # - atc
    descs['chembl'].update(actlvl1=[], actlvl2=[], actlvl3=[], actlvl4=[], actlvl5=[])
    for c in cmpd['atc_classifications']:
        descs['chembl']['actlvl1'].append(c[0:1])
        descs['chembl']['actlvl2'].append(c[0:3])
        descs['chembl']['actlvl3'].append(c[0:4])
        descs['chembl']['actlvl4'].append(c[0:5])
        descs['chembl']['actlvl5'].append(c)
    descs['chembl']['actlvl1'] = list(set(descs['chembl']['actlvl1']))
    descs['chembl']['actlvl2'] = list(set(descs['chembl']['actlvl2']))
    descs['chembl']['actlvl3'] = list(set(descs['chembl']['actlvl3']))
    descs['chembl']['actlvl4'] = list(set(descs['chembl']['actlvl4']))
    descs['chembl']['actlvl5'] = list(set(descs['chembl']['actlvl5']))
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
    print(descs)


test("CHEMBL457299")
