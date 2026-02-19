from rest_framework import serializers
from .models import BaseItem, UniqueItem, UniqueAncientMeta, League

class BaseItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = BaseItem
    fields = ["id", "name", "item_class", "slot","icon_url"]

class UniqueItemMetaSerializer(serializers.ModelSerializer):
  class Meta:
    model = UniqueAncientMeta
    fields = ["pool", "tier", "chance", "avg_orbs", "min_ilvl", "source"]

class UniqueItemListSerializer(serializers.ModelSerializer):
  base_item = BaseItemSerializer(read_only=True)
  ancient_meta = UniqueItemMetaSerializer(read_only=True)

  chaos_value = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True, required=False)
  divine_value = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True, required=False)
  listing_count = serializers.IntegerField(read_only=True, required=False)


  class Meta:
    model = UniqueItem
    fields = [
      "id", 
      "name", 
      "required_level",
      "image_url", 
      "base_item", 
      "chaos_value", 
      "divine_value", 
      "listing_count",
      "flavour_text", 
      "ancient_meta"]

class UniqueItemDetailSerializer(serializers.ModelSerializer):
  base_item = BaseItemSerializer(read_only=True) 
  ancient_meta = UniqueItemMetaSerializer(read_only=True)

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
    "ancient_meta",
    ]