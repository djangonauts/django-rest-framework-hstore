from rest_framework import viewsets
from rest_framework import routers

from .models import *
from .serializers import *


class DataBagViewSet(viewsets.ModelViewSet):
    model = DataBag
    serializer_class = DataBagSerializer


class SchemaDataBagViewSet(viewsets.ModelViewSet):
    model = SchemaDataBag
    serializer_class = SchemaDataBagSerializer


class SchemaHStoreViewSet(viewsets.ModelViewSet):
    model = SchemaDataBag
    serializer_class = SchemaHStoreSerializer


router = routers.SimpleRouter()
router.register(r'databag', DataBagViewSet)
router.register(r'schemadatabag', SchemaDataBagViewSet)
router.register(r'schemahstore', SchemaHStoreViewSet)
urlpatterns = router.urls
