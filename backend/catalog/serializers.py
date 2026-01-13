from rest_framework import serializers
from .models import BaseItem, UniqueItem

class BaseItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = BaseItem
    fields = ["id", "name", "item_class", "slot"]

class UniqueItemListSerializer(serializers.ModelSerializer):
  base_item = BaseItemSerializer(read_only=True)

  class Meta:
    model = UniqueItem
    fields = ["id", "name", "required_level","image_url", "base_item"]

class UniqueItemDetailSerializer(serializers.ModelSerializer):
  base_item = BaseItemSerializer(read_only=True) 

  class Meta:
    model = UniqueItem
    fields = [
    "id",
    "name",
    "required_level",
    "image_url",
    "flavour_text",
    "raw_mods",
    "base_item",
    "created_at",
    ]