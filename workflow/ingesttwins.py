""" ingest all chemtwins in sciflow """
import os
import django
import requests
import jena_functions

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

alltwins = requests.get("https://sds.coas.unf.edu/sciflow/files/twinlist").json()
for key, url in alltwins.items():
    resp = jena_functions.addgraph(url)
    if resp == "success":
        print("File '" + url + "' added")
    else:
        print("File '" + url + "' not added")
        print(resp)
exit()
