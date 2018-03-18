# Django core
from django.contrib import admin

# Models
from .models import (Game, UserGameAction)

# Core django admin site register
admin.site.register(Game)
admin.site.register(UserGameAction)
