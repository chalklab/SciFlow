"""django unit test file"""
from django.test import TestCase
from datafiles.models import *
import json


class AddfileTestCase(TestCase):
    def setUp(self):
        """unittest setup"""
        JsonLookup.objects.create(
            id=999,
            dataset_id=1,
            uniqueid="chalklab:example:ph",
            title="pH of cyanide standard",
            graphname="https://stuchalk.github.io/chalklab/examples/ph/",
            currentversion=1,
            auth_user_id=2
        )
        with open('datafiles/test.jsonld') as ld:
            jsonld = json.load(ld)

        JsonFiles.objects.create(
            json_lookup_id=999,
            file=json.dumps(jsonld, separators=(',', ':')),
            type="raw",
            version=1
        )

    def test_addfile(self):
        """unittest verification"""
        meta = JsonLookup.objects.get(id=999)
        file = JsonFiles.objects.get(json_lookup_id=999)
        self.assertEqual(meta.title, 'pH of cyanide standard')
        self.assertEqual(file.type, 'raw')
