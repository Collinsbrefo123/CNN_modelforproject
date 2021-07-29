from django.contrib import admin
from .models import TowerName, CorridorLine

# Register your models here.
admin.site.register([TowerName, CorridorLine], )
