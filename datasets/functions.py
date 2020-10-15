"""functions to support dataset view functions"""
from datafiles.functions import *
from pathlib import Path
from sciflow.settings import *


def testimport():
    """ import test data from static/files in the DB"""
    folder = Path(BASE_DIR + "/static/files/")
    for file in folder.iterdir():
        if str(file).endswith('.jsonld'):
            filename = str(file).split("\\")[-1]
            filetype = None
            with open(filename, "r") as f:
                data = json.load(f)
            if "/aspect/" in data["@id"]:
                filetype = "aspect"
            elif "/data/" in data["@id"]:
                filetype = "data"
            elif "/facet/" in data["@id"]:
                filetype = "facet"

            if addfile({"path": filename}, filetype):
                print("Imported " + filename)
