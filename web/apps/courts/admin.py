from django.contrib import admin
from .models import (Court, CourtType, Country, City, Place)


admin.site.register(Court)
admin.site.register(CourtType)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Place)
