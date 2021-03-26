"""serializer file for substances"""
from rest_framework import serializers
from substances.models import *


class SubstancesSerializer(serializers.ModelSerializer):
    """serailizer for the substances table"""

    class Meta:
        """meta fields"""
        model = Substances
        fields = '__all__'
        extra_fields = ['identifiers_set', 'sources_set', 'descriptors_set']
        depth = 1

    def get_field_names(self, declared_fields, info):
        """field names"""
        expanded_fields = super(SubstancesSerializer, self).\
            get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields
