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
    class Meta:
        model = SchemaDataBag
