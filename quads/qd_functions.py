"""quad table function library"""
from quads.models import Quads


def add(quad):
    """adds a quad to the table"""
    q = quad.replace(' .', '').replace('> ', '>*').replace('" <', '"*<').split('*')
    if len(q) == 4:
        Quads.objects.get_or_create(sub=q[0], prd=q[1], obj=q[2], gph=q[3])
    elif len(q) == 3:
        Quads.objects.get_or_create(sub=q[0], prd=q[1], obj=q[2], gph=None)
    return


def find(type, text):
    filter_kwargs = {"{}__icontains".format(type): text}
    hits = Quads.objects.values(type).filter(**filter_kwargs)
    return hits


def addbulk(quads):
    objs = [
        Quads(sub=q[0], prd=q[1], obj=q[2], gph=q[3])
        for q in quads
    ]
    # print(objs)
    Quads.objects.bulk_create(objs)
    return
