from django import forms
from playerapp import models
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = models.Register
        fields = "__all__"