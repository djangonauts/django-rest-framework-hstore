from rest_framework import viewsets
from rest_framework import routers

from .models import *
from .serializers import *


class DataBagViewSet(viewsets.ModelViewSet):
    queryset = DataBag.objects.all()
    serializer_class = DataBagSerializer


class SchemaDataBagViewSet(viewsets.ModelViewSet):
    queryset = SchemaDataBag.objects.all()
    serializer_class = SchemaDataBagSerializer


router = routers.SimpleRouter()
router.register(r'databag', DataBagViewSet)
router.register(r'schemadatabag', SchemaDataBagViewSet)
urlpatterns = router.urls
