from django.contrib import admin
from adminapp import models
from .models import VisitorCounter, VenueDetails, HostedGame  


# Register your models here.
admin.site.register(models.VenueList)
admin.site.register(models.Game_Category_List)
admin.site.register(models.VenueGames)
admin.site.register(models.VenueDetails)
admin.site.register(models.HostedGame)
admin.site.register(models.Notification)
admin.site.register(models.Booking)
admin.site.register(models.VenueGamePrice)




class VenueDetailsAdmin(admin.ModelAdmin):
    list_display = ('venue', 'opening_time', 'closing_time')  # Use actual fields

