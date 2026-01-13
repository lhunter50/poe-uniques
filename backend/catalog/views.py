from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .models import BaseItem, UniqueItem
from .serializers import (
  BaseItemSerializer,
  UniqueItemListSerializer,
  UniqueItemDetailSerializer
)

class BaseItemViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = BaseItem.objects.all().order_by("name")
  serializer_class = BaseItemSerializer
  filter_backends = [filters.SearchFilter]
  search_fields = ["name", "slot", "item_class"]
  