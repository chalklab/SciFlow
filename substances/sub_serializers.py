import os
import django
from rest_framework.relations import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

import json
from rest_framework import serializers
from substances.models import *

class SubstancesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Substances
        fields = '__all__'
        extra_fields = ['identifiers_set', 'sources_set', 'descriptors_set']
        depth = 1

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(SubstancesSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


# x = SubstancesSerializer()
# print(repr(x))

test = SubstancesSerializer(Substances.objects.last())
print(json.dumps(test.data, indent=4))