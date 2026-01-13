from django.db import models
from django.utils import timezone


class BaseItem(models.Model):
  class ItemClass(models.TextChoices):
    WEAPON = "weapon", "Weapon"
    ARMOUR = "armour", "Armour"
    ACCESSORY = "accessory", "Accessory"
    JEWEL = "jewel", "Jewel"
    FLASK = "flask", "Flask"
    OTHER = "other", "Other"

  class Slot(models.TextChoices):
    HELMET = "helmet", "Helmet"
    BODY = "body", "Body Armour"
    GLOVES = "gloves", "Gloves"
    BOOTS = "boots", "Boots"
    SHIELD = "shield", "Shield"
    WEAPON = "weapon", "Weapon"
    BELT = "belt", "Belt"
    RING = "ring", "Ring"
    AMULET = "amulet", "Amulet"
    JEWEL = "jewel", "Jewel"
    FLASK = "flask", "Flask"
    OTHER = "other", "Other"


  name = models.CharField(max_length=200)
  item_class = models.CharField(max_length=20, choices=ItemClass.choices, default=ItemClass.OTHER)
  slot = models.CharField(max_length=20, choices=Slot.choices, default=Slot.OTHER) #eg Ring, Helmet, Bow, etc.


  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=["name", "item_class"],
        name="uniq_baseitem_name_class",
      )
    ]
    indexes = [
      models.Index(fields=["item_class", "slot"]),
      models.Index(fields=["name"]),
    ]

  def __str__(self):
    return self.name

class UniqueItem(models.Model):
  name = models.CharField(max_length=200, db_index=True)
  base_item = models.ForeignKey(BaseItem, on_delete=models.PROTECT, related_name="uniques")
  poe_ninja_id = models.IntegerField(null=True, blank=True, unique=True, db_index=True)
  
  required_level = models.PositiveIntegerField(null=True, blank=True)
  image_url = models.URLField(blank=True, default="")

  flavour_text = models.TextField(blank=True, default="")
  raw_mods = models.TextField(blank=True, default="")

  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name
  
class League(models.Model):
  """
  A league name as used by poe.ninja (e.g: Settlers, Affliction, etc.)
  """
  name = models.CharField(max_length=100, unique=True)
  is_active = models.BooleanField(default=False)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
  
class UniqueItemLeaguePresence(models.Model):
  """
  Marks that a Unique Item was observed in a given League
  """

  unique_item = models.ForeignKey(
    "UniqueItem",
    on_delete=models.CASCADE,
    related_name="league_presence"
  )
  league = models.ForeignKey(
    League,
    on_delete=models.CASCADE,
    related_name="unique_presence"
  )

  first_seen_at = models.DateField(default=timezone.localdate)
  last_seen_at = models.DateField(default=timezone.localdate)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=["unique_item", "league"],
        name="uniq_uniqueitem_league"
      )
    ]
    indexes = [
      models.Index(fields=["league", "last_seen_at"]),
      models.Index(fields=["unique_item", "league"])
    ]
  
  def __str__(self):
    return f"{self.unique_item} @ {self.league}"