from django.contrib import admin
from .models import TowerName, CorridorLine,TowerImages

# Register your models here.
admin.site.register([TowerName, CorridorLine, TowerImages], )
