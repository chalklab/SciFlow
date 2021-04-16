""" serializers for reports data"""
from rest_framework import serializers
from datafiles.models import *


class JsonFileSerializer(serializers.ModelSerializer):
    """ reports serializer """
    class Meta:
        """ settings """
        model = JsonFiles
        fields = '__all__'
        depth = 1


class JsonLookupSerializer(serializers.ModelSerializer):
    """json_lookup serializer"""
    vers = JsonFileSerializer(source='jsonfiles_set', many=True, required=False)

    class Meta:
        """ settings """
        model = JsonLookup
        fields = '__all__'
        depth = 1


class DatasetSerializer(serializers.ModelSerializer):
    """ reports serializer """
    files = JsonLookupSerializer(source='jsonlookup_set', many=True, required=False)

    class Meta:
        """ settings """
        model = Datasets
        fields = '__all__'
        depth = 1
