from django.db import models

# Create your models here.
class Register(models.Model):
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    contact = models.IntegerField()
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    password = models.CharField(max_length=16)
    cpassword = models.CharField(max_length=16)