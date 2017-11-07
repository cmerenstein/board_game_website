from django import forms
from django.core import validators
from django.contrib.auth.models import User
from sun_tzu.models import UserProfileInfo, Game

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta():
		model = User
		fields = ('username', 'email', 'password')

class GameForm(forms.ModelForm):
	botcatcher = forms.CharField(required=False,
								widget=forms.HiddenInput,
								validators=[validators.MaxLengthValidator(0)])
	
	class Meta:
		model = Game
		fields = ('player_one', 'player_two')