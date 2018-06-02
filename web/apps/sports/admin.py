# Django core
from django.contrib import admin

# Models
from .models import Amplua, GameType, SportType

# Core django admin site register
admin.site.register(SportType)
admin.site.register(GameType)
admin.site.register(Amplua)
