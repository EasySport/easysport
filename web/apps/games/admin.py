# Django core
from django.contrib import admin

# Models
from .models import Game, UserGameAction


class ActionsInline(admin.TabularInline):
    model = UserGameAction
    extra = 0


class GameAdmin(admin.ModelAdmin):
    inlines = [
        ActionsInline,
    ]
    list_filter = ('is_reported', 'datetime')


# Core django admin site register
admin.site.register(Game, GameAdmin)
admin.site.register(UserGameAction)
