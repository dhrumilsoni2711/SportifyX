from django.db import models

# Create your models here.
class VenueList(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    contact = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    image = models.FileField(upload_to='venueimages/')
    status = models.BooleanField(default=True)

class GameList(models.Model):
    name = models.CharField(max_length=50)
    Level = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    image = models.FileField(upload_to='gameimages/')
    rules = models.TextField()
    