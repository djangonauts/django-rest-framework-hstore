from rest_framework import serializers
from rest_framework_hstore.fields import DictionaryField
from .models import *


__all__ = [
    'DataBagSerializer',
    'SchemaDataBagSerializer'
]


class DataBagSerializer(serializers.ModelSerializer):
    data = DictionaryField()
    class Meta:
        model = DataBag


class SchemaDataBagSerializer(serializers.ModelSerializer):
    data = DictionaryField(schema=True)
    class Meta:
        #fields = ['name', 'data']
        model = SchemaDataBag