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