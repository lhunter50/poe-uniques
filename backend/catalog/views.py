from django.db.models import Exists, OuterRef, Subquery, F, Case, When, Value, IntegerField
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from .models import BaseItem, UniqueItem, UniqueItemLeaguePresence, League, UniqueItemLeagueStats
from .serializers import (
  BaseItemSerializer,
  UniqueItemListSerializer,
  UniqueItemDetailSerializer,
)

class UniquePagination(PageNumberPagination):
  page_size = 18

def get_current_league() -> League:
  # For now I will use this, will be able to update this do auto detect current leagues
  league = League.objects.filter(is_active=True).first()

  if not league:
    raise ValidationError(
      {"league": "No active league set."}
    )
  
  return league

class BaseItemViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = BaseItem.objects.all().order_by("name")
  serializer_class = BaseItemSerializer
  filter_backends = [filters.SearchFilter]
  search_fields = ["name", "slot", "item_class"]

class UniqueItemViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = UniqueItem.objects.select_related("base_item").all().order_by("name")
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
  pagination_class = UniquePagination

  filterset_fields = {
    "base_item": ["exact"],
    "required_level": ["exact", "gte", "lte"],
    "base_item__slot": ["exact"],
    "base_item__item_class": ["exact"],
  }

  search_fields = ["name", "base_item__name"]

  ordering_fields = [
    "name", 
    "required_level", 
    "created_at",
    "chaos_value",
    "divine_value",
    "listing_count",
    "ancient_meta__tier"
  ]
  
  ordering = [
    "has_ancient",
    F("ancient_meta__tier").asc(nulls_last=True),
    F("chaos_value").desc(nulls_last=True),
    "name"
  ]

  def _get_league(self) -> League:
    league_name =(self.request.query_params.get("league") or "" ).strip()
    if league_name:
      return get_object_or_404(League, name=league_name)
    
    return get_current_league()
  
  def list (self, request, *args, **kwargs):
    league = self._get_league()

    queryset = self.filter_queryset(self.get_queryset())

    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      resp = self.get_paginated_response(serializer.data)

      resp.data["meta"] = {
        "league": {"id": league.id, "name": league.name}
      }
      return resp
    
    serializer = self.get_serializer(queryset, many=True)
    return Response({
      "meta": {"league": {"id": league.id, "name": league.name}},
      "results": serializer.data
    })

  def get_queryset(self):
    """

    """
    league = self._get_league()

    qs = UniqueItem.objects.select_related("base_item", "ancient_meta")

    current_presence = UniqueItemLeaguePresence.objects.filter(
      unique_item_id=OuterRef("pk"),
      league_id = league.id
    )

    qs = qs.annotate(_in_league=Exists(current_presence)).filter(_in_league=True)

    stats_qs = UniqueItemLeagueStats.objects.filter(
      unique_item_id=OuterRef("pk"),
      league_id=league.id,
    ).order_by("-last_fetched_at")

    qs = qs.annotate(
      chaos_value=Subquery(stats_qs.values("chaos_value")[:1]),
      divine_value=Subquery(stats_qs.values("divine_value")[:1]),
      listing_count=Subquery(stats_qs.values("listing_count")[:1]),
    )

    qs = qs.annotate(
      has_ancient=Case(
          When(ancient_meta__isnull=False, then=Value(0)),
          default=Value(1),
          output_field=IntegerField(),
      )
    )

    return qs

  def get_serializer_class(self):
    if self.action == "retrieve":
      return UniqueItemDetailSerializer
    return UniqueItemListSerializer