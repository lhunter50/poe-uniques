from django.db import models

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