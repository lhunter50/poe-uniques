from django.db import models
from django.utils import timezone


class BaseItem(models.Model):
  class ItemClass(models.TextChoices):
    WEAPON = "weapon", "Weapon"
    ARMOUR = "armour", "Armour"
    ACCESSORY = "accessory", "Accessory"
    JEWEL = "jewel", "Jewel"
    FLASK = "flask", "Flase"
    OTHER = "other", "Other"

  name = models.CharField(max_length=200, unique=True)
  item_class = models.CharField(max_length=20, choices=ItemClass.choices, default=ItemClass.OTHER)
  slot = models.FloatField(max_length=100, blank=True, default="") #eg Ring, Helmet, Bow, etc.

  def __str__(self):
    return self.name

class UniqueItem(models.Model):
  name = models.CharField(max_length=200, unique=True)
  base_item = models.ForeignKey(BaseItem, on_delete=models.PROTECT, related_name="uniques")
  
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

  created_at = models.DateTimeField(auto_now=True)

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

  first_seen_at = models.DateField(default=timezone.now)
  last_seen_at = models.DateField(default=timezone.now)

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