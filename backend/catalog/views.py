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

class UniqueItemViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = UniqueItem.objects.select_related("base_item").all().order_by("name")
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

  filterset_fields = {
    "base_item": ["exact"],
    "required_level": ["exact", "gte", "lte"],
    "base_item__slot": ["exact"],
    "base_item__item_class": ["exact"],
  }

  search_fields = ["name", "required_level", "created_at"]
  ordering = ["name"]

  def get_serializer_class(self):
    if self.action == "retrieve":
      return UniqueItemDetailSerializer
    return UniqueItemListSerializer