from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Game_Category_List(models.Model):
    game_name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.FileField(upload_to='categoryimages/')


class VenueList(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    image = models.FileField(upload_to='venueimages/')
    status = models.BooleanField(default=True)
    location = models.URLField(null=True,blank=True)
    

class VenueGames(models.Model):
    venue = models.ForeignKey(VenueList, on_delete=models.CASCADE)
    game_category = models.ForeignKey(Game_Category_List,on_delete=models.CASCADE) 

# class PlayEvent(models.Model):
#     event_name = models.CharField(max_length=50)
#     date = models.DateField()
#     time = models.TimeField()
#     address = models.ForeignKey(VenueList, on_delete=models.CASCADE)


# <iframe src="{{https://www.google.com/maps/embed?pb=!1m16!1m12!1m3!1d3719.997464901475!2d72.51329497536825!3d23.01706722917769!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!2m1!1sAangan%20Banquet%2C%202nd%20Floor%2C%20Satellite%2C%20opposite%20Nandanvan%204%2C%20Jodhpur%20Village%2C%20Ahmedabad%2C%20Gujarat%20380051!5e1!3m2!1sen!2sin!4v1739171982017!5m2!1sen!2sin}}" width="400" height="300" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>


class VisitorCounter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    visited_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)  # Store the timestamp of the visit

class VenueDetails(models.Model):
    venue = models.OneToOneField(VenueList, on_delete=models.CASCADE, related_name='details')  # Link to VenueList
    venue_description = models.TextField()
    venue_amenities = models.JSONField(default=list)
    venue_time = models.TimeField(null=True, blank=True)





