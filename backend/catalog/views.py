import os

from django.db.models import Exists, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .models import BaseItem, UniqueItem, UniqueItemLeaguePresence, League
from .serializers import (
  BaseItemSerializer,
  UniqueItemListSerializer,
  UniqueItemDetailSerializer
)

STANDARD_LEAGUE_NAME = "Standard"

def get_current_league_name() -> str:
  # For now I will use this, will be able to update this do auto detect current leagues
  return os.getenv("CURRENT_LEAGUE", "").strip() or STANDARD_LEAGUE_NAME

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

  search_fields = ["name", "base_item__name"]
  ordering_fields = ["name", "required_level", "created_at"]
  ordering = ["name"]

  def get_queryset(self):
    """
    view=all -> items present in Standard (all)
    view=current -> items present in CURRENT_LEAGUE
    view=current_only -> items present in CURRENT_LEAGUE and NOT in Standard (rare occasion)
    default -> is the same as view=all
    """
    qs = UniqueItem.objects.select_related("base_item").all()

    view = (self.request.query_params.get("view") or "all").strip().lower()
    current_league = get_current_league_name()

    standard_presence = UniqueItemLeaguePresence.objects.filter(
      unique_item_id=OuterRef("pk"),
      league__name=STANDARD_LEAGUE_NAME,
    )
    current_presence = UniqueItemLeaguePresence.objects.filter(
      unique_item_id=OuterRef("pk"),
      league__name = current_league
    )

    if view == "current":
      qs = qs.annotate(_present=Exists(current_presence)).filter(_present=True)
    elif view == "currently_only":
      qs = qs.annotate(
        _in_current=Exists(current_presence),
        _in_standard=Exists(standard_presence),
      ).filter(_in_current=True, _in_standard=False)
    else:
      # all (standard)
      qs = qs.annotate(_present=Exists(standard_presence)).filter(_present=True)
    return qs.order_by("name")

  def get_serializer_class(self):
    if self.action == "retrieve":
      return UniqueItemDetailSerializer
    return UniqueItemListSerializer