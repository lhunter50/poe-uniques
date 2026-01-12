from rest_framework import serializers
from .models import BaseItem, UniqueItem

class BaseItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = BaseItem
    fields = ["id", "name", "item_class", "slot"]

class UniqueItemListSerializer(serializers.ModelSerializer):
  