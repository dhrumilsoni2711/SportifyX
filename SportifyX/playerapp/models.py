from django.db import models
from django.contrib.auth.models import AbstractUser



# # Create your models here.
class User(AbstractUser):
    ADMIN = 'admin'
    PLAYER = 'player'

    contact = models.BigIntegerField(null=True,blank=True)
    gender = models.CharField(max_length=10,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    role = models.CharField(max_length=20, default=PLAYER,blank=True,null=True)

# GPS Location for Player
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Player's Sport
    sport = models.CharField(max_length=50, null=True, blank=True)