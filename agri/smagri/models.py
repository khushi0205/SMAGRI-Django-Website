from django.db import models

# Create your models here.
class Crop(models.Model):
    name = models.CharField(max_length = 255)
    planting_season = models.TextField()
    regions = models.TextField()
    introduction = models.TextField()
