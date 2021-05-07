import os
import django
from rest_framework import serializers
from datafiles.models import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()


class AspectLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AspectLookup
        fields = '__all__'
        extra_fields = ['aspectfiles_set', 'aspecterrors_set', 'aspectactlog_set']
        depth = 1

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(AspectLookupSerializer, self).get_field_names(declared_fields, info)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class FacetLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacetLookup
        fields = '__all__'
        extra_fields = ['facetfiles_set', 'faceterrors_set', 'facetactlog_set']
        depth = 1

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(FacetLookupSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class JsonAspectsSerializer(serializers.ModelSerializer):
    aspect_lookup = AspectLookupSerializer()
    facet_lookup = FacetLookupSerializer()

    class Meta:
        model = JsonAspects
        fields = '__all__'
        # extra_fields = ['']
        depth = 1


class JsonFacetsSerializer(serializers.ModelSerializer):
    facet_lookup = FacetLookupSerializer()

    class Meta:
        model = JsonFacets
        fields = '__all__'
        # extra_fields = ['']
        depth = 1


class JsonLookupSerializer(serializers.ModelSerializer):
    json_aspects = JsonAspectsSerializer(source="jsonaspects_set", many=True)
    json_facets = JsonFacetsSerializer(source="jsonfacets_set", many=True)

    class Meta:
        model = JsonLookup
        fields = '__all__'
        extra_fields = ['jsonerrors_set', 'jsonactlog_set']
        depth = 2

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(JsonLookupSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class JsonFilesSerializer(serializers.ModelSerializer):
    json_lookup = JsonLookupSerializer()

    class Meta:
        model = JsonFiles
        fields = '__all__'
        depth = 2
