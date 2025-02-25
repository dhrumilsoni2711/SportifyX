from django.contrib import admin
from adminapp import models
from .models import VisitorCounter,VenueDetails


# Register your models here.
admin.site.register(models.VenueList)
admin.site.register(models.Game_Category_List)
admin.site.register(models.VenueGames)


@admin.register(VenueDetails)
class VenueDetailsAdmin(admin.ModelAdmin):
    list_display = ('venue', 'venue_time')