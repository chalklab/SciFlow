from django.core.exceptions import ValidationError
import json

def json_validator(json_file):
    # json_file_content = json_file.read()
    json_file_content = json.load(json_file)
    keys_a = []
    keys_b = []
    isscidata = True
    if not str(json_file).endswith('.jsonld'):
        isscidata = False
    for k, v in json_file_content.items():
        keys_a.append(k)
        if k == '@graph':
            for y, z in v.items():
                keys_b.append(y)
    for y in ['@context', '@id', '@graph']:
        if y not in keys_a:
            isscidata = False
    for y in ['scidata']:
        if y not in keys_b:
            isscidata = False
    if not isscidata:
        raise ValidationError("Not Valid SciData JSON-LD")


