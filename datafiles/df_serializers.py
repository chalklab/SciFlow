""" serializer for datafiles """
from rest_framework import serializers
from datafiles.models import *


class AspectLookupSerializer(serializers.ModelSerializer):
    """serializer for the aspect_lookup table"""

    class Meta:
        """meta settings"""
        model = AspectLookup
        fields = '__all__'
        extra_fields = ['aspectfiles_set', 'aspecterrors_set', 'aspectactlog_set']
        depth = 1

    def get_field_names(self, declared_fields, info):
        """field_names"""
        expanded_fields = super(AspectLookupSerializer, self).get_field_names(declared_fields, info)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class FacetLookupSerializer(serializers.ModelSerializer):
    """serializer for the facet_lookup table"""

    class Meta:
        """meta settings"""
        model = FacetLookup
        fields = '__all__'
        extra_fields = ['facetfiles_set', 'faceterrors_set', 'facetactlog_set']
        depth = 1

    def get_field_names(self, declared_fields, info):
        """field_names"""
        expanded_fields = super(FacetLookupSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class JsonAspectsSerializer(serializers.ModelSerializer):
    """serializer for the json_aspects table"""
    aspect_lookup = AspectLookupSerializer()
    facet_lookup = FacetLookupSerializer()

    class Meta:
        """meta settings"""
        model = JsonAspects
        fields = '__all__'
        # extra_fields = ['']
        depth = 1


class JsonFacetsSerializer(serializers.ModelSerializer):
    """serializer for the json_facets table"""
    facet_lookup = FacetLookupSerializer()

    class Meta:
        """meta settings"""
        model = JsonFacets
        fields = '__all__'
        # extra_fields = ['']
        depth = 1


class JsonFilesSerializer(serializers.ModelSerializer):
    """serializer for the json_files table"""

    class Meta:
        """meta settings"""
        model = JsonFiles
        fields = '__all__'
        depth = 2


class JsonLookupSerializer(serializers.ModelSerializer):
    """serializer for the json_lookups table"""
    json_aspects = JsonAspectsSerializer(source="jsonaspects_set", many=True, required=False)
    json_facets = JsonFacetsSerializer(source="jsonfacets_set", many=True, required=False)
    vers = JsonFilesSerializer(source='jsonfiles_set', many=True, required=False)

    class Meta:
        """meta settings"""
        model = JsonLookup
        fields = '__all__'
        extra_fields = ['jsonerrors_set', 'jsonactlog_set']
        depth = 2

    def get_field_names(self, declared_fields, info):
        """field_names"""
        expanded_fields = super(JsonLookupSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class DatasetSerializer(serializers.ModelSerializer):
    """ datasets serializer """
    files = JsonLookupSerializer(source='jsonlookup_set', many=True, required=False)

    class Meta:
        """ settings """
        model = Datasets
        fields = '__all__'
        depth = 1


class ReferencesSerializer(serializers.ModelSerializer):
    """ references serializer """
    files = JsonLookupSerializer(source='jsonlookup_set', many=True, required=False)

    class Meta:
        """ settings """
        model = References
        fields = '__all__'
        depth = 1
