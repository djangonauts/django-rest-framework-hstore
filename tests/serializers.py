from rest_framework import serializers
from rest_framework_hstore.fields import DictionaryField
from rest_framework_hstore.serializers import HStoreSerializer

from .models import *


__all__ = [
    'DataBagSerializer',
    'SchemaDataBagSerializer',
    'SchemaHStoreSerializer'
]


class DataBagSerializer(serializers.ModelSerializer):
    data = DictionaryField()
    class Meta:
        fields = ['name', 'data']
        model = DataBag


class SchemaDataBagSerializer(serializers.ModelSerializer):
    data = DictionaryField(schema=True)
    class Meta:
        model = SchemaDataBag


class SchemaHStoreSerializer(HStoreSerializer):
    data = DictionaryField(schema=True)
    class Meta:
        model = SchemaDataBag
