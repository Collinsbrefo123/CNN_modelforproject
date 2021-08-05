from django.db import models


# Create your models here.

class CorridorLine(models.Model):
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    source_coordinate_lat = models.FloatField(max_length=200, null=True)
    source_coordinate_long = models.FloatField(max_length=200, null=True)
    destination_coordinate_lat = models.FloatField(max_length=200, null=True)
    destination_coordinate_long = models.FloatField(max_length=200, null=True)

    def __str__(self):
        return self.name


class TowerName(models.Model):
    towername = models.CharField(max_length=200)
    latitude = models.FloatField(max_length=200)
    longitude = models.FloatField(max_length=200)
    line = models.ForeignKey(CorridorLine, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.towername


class TowerImages(models.Model):
    towerlocation = models.CharField(max_length=100, null=True)
    towerimage = models.ImageField(upload_to='media')

    def __str__(self):
        return self.towerlocation
