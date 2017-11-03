from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
	user = models.OneToOneField(User)
	
	def __str__(self):
		return self.user.username
		

class Game(models.Model):
	game_id = models.IntegerField(unique=True, primary_key=True)
	player_one = models.ForeignKey(UserProfileInfo, related_name="p1")
	player_two = models.ForeignKey(UserProfileInfo, related_name="p2")
	
	turn = models.IntegerField(default=0)
	score = models.IntegerField(default=0)

class Province(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	name = models.CharField(max_length = 16)
	player_control = models.CharField(max_length = 256, default="")
	
	round_one_points = models.IntegerField()
	round_two_points = models.IntegerField()
	round_three_points = models.IntegerField()
	
class Player(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	card_number = models.IntegerField() # Keeps track of how much of the deck has been taken
	
	player_name = models.CharField(max_length = 256)
	
class Card(models.Model):
	deck_position = models.IntegerField()
	is_single_use = models.BooleanField()
	