from django import forms
from adminapp import models 
class VenueListform(forms.ModelForm):
    class Meta:
        model = models.VenueList
        fields = "__all__"
        # exclude = ['status']