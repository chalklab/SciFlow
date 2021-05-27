"""quad table function library"""
from quads.models import Quads
import pyld
import json

def ingest(upload, user):
    """function to ingest JSON-LD, convert it to quads, and save in the quads table"""
    if str(upload).endswith('.jsonld'):
        upload.seek(0)
        text = upload.read()
        file = json.loads(text)


def add(q):
    """adds a quad to the table"""
    quad = Quads(s=q['s'], p=q['p'], o=q['o'], g=q['s'])
    quad.save()
    return
