"""quad table function library"""
from quads.models import Quads
import json
import hashlib


def ingest(upload, user):
    """function to ingest JSON-LD, convert it to quads, and save in the quads table"""
    if str(upload).endswith('.jsonld'):
        upload.seek(0)
        text = upload.read()
        file = json.loads(text)


def add(quad):
    """adds a quad to the table"""
    q = quad.replace(' .', '').replace('> ', '>*').replace('" <', '"*<').split('*')
    if len(q) == 4:
        Quads.objects.get_or_create(sub=q[0], prd=q[1], obj=q[2], gph=q[3])
    elif len(q) == 3:
        Quads.objects.get_or_create(sub=q[0], prd=q[1], obj=q[2])
    return