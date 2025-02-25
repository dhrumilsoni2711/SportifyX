from django import forms
from adminapp import models
# from django.contrib.auth.models import User

class VenueListForm(forms.ModelForm):
    class Meta:
        model = models.VenueList
        fields = "__all__"

class GameCategoryListForm(forms.ModelForm):
    class Meta:
        model = models.Game_Category_List
        fields = "__all__"

class VenueGamesform(forms.ModelForm):
        class Meta:
             model = models.VenueGames
             exclude = ['venue','game_category']
            #  fields = "__all__"