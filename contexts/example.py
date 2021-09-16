"""example functions for development"""
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()


from contexts.ols_functions import *
from contexts.views import *
from contexts.ctx_functions import *
from scipy.io import loadmat
import pandas as pd


# test crosswalk list
cwk = True
if cwk:
    getcwks(3)
    exit()

# test GitHub access
gh = True
if gh:
    test = '{"@context": [{"@vocab": "https://www.w3.org/2001/XMLSchema#",' \
           '"sdo": "https://stuchalk.github.io/scidata/ontology/scidata.owl#",' \
           '"condition": {"@id": "sdo:condition"}}]}'
    addctxfile('contexts/test.jsonld', 'test commit via API', test)
    exit()

# test matlab file import
mlab = False
if mlab:
    file = loadmat('/Users/n00002621/Dropbox/Grants/Funded/NIST KnowLedger 2021 - 2022/Data/AmBench 2018/sam_0_output.mat')
    data = [[row.flat[0] for row in line] for line in file['ans'][0]]
    width = 320
    pd.set_option('display.width', width)
    pd.set_option('display.max_columns', 12)
    table = pd.DataFrame(data)
    print(table.head())
    exit()

# test ChEMBL API
chembl = False
if chembl:
    out = ctxonts()
    print(out)
    exit()

# add a new substance to the database
nslist = False
if nslist:
    nslist = getnsps()
    print(nslist)
    exit()

term = False
if term:
    data = getont(13)
    print(data.sdsection)
    exit()
