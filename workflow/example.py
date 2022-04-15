""" example code """
import os
import django
import jena_functions

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

# search for all graphs
resp = jena_functions.tcount()
print(resp)
exit()
