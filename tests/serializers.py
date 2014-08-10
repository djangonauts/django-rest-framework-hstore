from rest_framework import serializers
from rest_framework_hstore.fields import HStoreField
from rest_framework_hstore.serializers import HStoreSerializer

from .models import *


__all__ = [
    'DataBagSerializer',
    'SchemaDataBagSerializer'
]


class DataBagSerializer(HStoreSerializer):
    class Meta:
        model = DataBag


class SchemaDataBagSerializer(HStoreSerializer):
    data = HStoreField(schema=True)
    class Meta:
        model = SchemaDataBag
