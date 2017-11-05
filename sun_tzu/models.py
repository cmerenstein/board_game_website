from django.db import models
from django.contrib.auth.models import User
import re

# Create your models here.
class UserProfileInfo(models.Model):
	user = models.OneToOneField(User)
	
	def __str__(self):
		return self.user.username
		

class Game(models.Model):
	game_id = models.IntegerField(unique=True, primary_key=True)
	player_one = models.ForeignKey(UserProfileInfo, related_name="p1")
	player_two = models.ForeignKey(UserProfileInfo, related_name="p2")
	
	turn = models.IntegerField(default=1)
	score = models.IntegerField(default=0)
	
	def __str__(self):
		return str(self.game_id)
	
	

class Province(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	name = models.CharField(max_length = 16)
	player_control = models.CharField(max_length = 256, default="")
	armies = models.IntegerField(default = 0) ## Positive = player one
	
	round_one_points = models.IntegerField()
	round_two_points = models.IntegerField()
	round_three_points = models.IntegerField()
	
	player_one_card = models.CharField(max_length = 3, default = "")
	player_two_card = models.CharField(max_length = 3, default = "")
	
	def __str__(self):
		return self.name
		
	def add_armies(self):
	## this is gonna get ugly...
		p_one_is_number = (re.match("^[0-9]+$", self.player_one_card) != None)
		p_two_is_number = (re.match("^[0-9]+$", self.player_two_card) != None)
	
		# both are numbers, add difference to armies
		if p_one_is_number and p_two_is_number:
			self.armies += (int(self.player_one_card) - int(self.player_two_card))
		
		# either player plays a "P"
		if "P" in self.player_one_card or "P" in self.player_two_card:
			self.armies = int(self.armies / 2)
		
		# p1 plays +1 or -1	
		elif p_two_is_number and not p_one_is_number:
			if "+" in self.player_one_card:
				self.armies += 1
			else:
				self.armies -= 1
		
		# p2 plays +1 or -1
		elif p_one_is_number and not p_two_is_number:
			if "+" in self.player_two_card:
				self.armies -= 1
			else:
				self.armies += 1
		
		return self.armies
		
class Player(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	card_number = models.IntegerField(default=0) # Keeps track of how much of the deck has been taken
	player_name = models.CharField(max_length = 256)
	turns_taken = models.IntegerField(default=0)
	
	def hand(self):
		# print(self.card_set.order_by("deck_position")[:self.card_number])
		return self.card_set.order_by("deck_position")[:self.card_number]
	
	def __str__(self):
		return self.player_name

		
class Card(models.Model):
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	deck_position = models.IntegerField()
	is_single_use = models.BooleanField()
	card_value = models.CharField(max_length = 3)
	
	def __str__(self):
		return self.card_value