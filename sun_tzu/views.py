from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from sun_tzu.forms import UserForm, GameForm
from .models import Game, Province, UserProfileInfo, Player, Card
import random

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
	
	return render(request, 'sun_tzu/index.html', {})

def my_games(request):

	player = get_object_or_404(UserProfileInfo, user=request.user)
	print(request.user, player)
	gameset = player.p1.all() | player.p2.all()
	print(gameset)
	return render(request, 'sun_tzu/my_games.html', {"gameset":gameset})
	
@login_required
def new_game(request):
	PROVINCES = ["Wu", "Han-Qi", "Jin-Yan", "Chu", "Qin"]
	BASE_CARDS = ["1", "2", "3", "4", "5", "6"]
	EXTRA_CARDS = ["+1", "+1", "+1", "-1", "-1", "-1", "P", "P", "P", "7", "8", "9", "10"]
	POINTS_CARDS = [[1, 2, 4], [1, 3, 5], [1, 4, 3], [2, 3, 4], [2, 3, 2], [2, 5, 2], [3, 1, 5], [3, 2, 3], [4, 3, 2]]
	
	if request.method == "POST":
		game_form = GameForm(data=request.POST)
		
		if game_form.is_valid():
			game = game_form.save()
			
			### give provinces values
			random.shuffle(POINTS_CARDS)
			for province in PROVINCES: 
				points_card = POINTS_CARDS.pop()
				r_one = points_card[0]
				r_two = points_card[1]
				r_three = points_card[2]
				game.province_set.create(name=province, round_one_points=r_one, round_two_points=r_two, round_three_points=r_three)
			
			### make player objects
			for player_user in [game.player_one, game.player_two]: 
				game.player_set.create(player_name = player_user.user.username)
			
			### give players cards
			for p in game.player_set.all():
				deck_position = 0
				for card in BASE_CARDS:
					p.card_set.create(card_value = card, is_single_use=False, deck_position = deck_position)
					deck_position += 1
				random.shuffle(EXTRA_CARDS)
				for card in EXTRA_CARDS:
					p.card_set.create(card_value = card, is_single_use=True, deck_position = deck_position)	
					deck_position += 1
				p.save()
			
			game.save()
			return HttpResponseRedirect(reverse('sun_tzu:game_view', kwargs={'game_id': game.game_id}))
	
	else:
		game_form = GameForm()
		
	return render(request, 'sun_tzu/new_game.html', {"form":game_form})

	
def game_view(request, game_id):
	game = get_object_or_404(Game, pk=game_id)
	
	context = {}
	context["game"] = game

	player_logged_in = False
	player_one = False
	if request.user == game.player_one.user or request.user == game.player_two.user:
		player_logged_in = True

		player_object = game.player_set.get(player_name=request.user.username)
		context["player_object"] = player_object
		if request.user == game.player_one.user:
			player_one = True
	
	context["player_logged_in"] = player_logged_in
	player_one_obj = game.player_set.get(player_name=game.player_one.user.username)
	player_two_obj = game.player_set.get(player_name=game.player_two.user.username)	

	
	if request.method == "POST":
		print(request.POST)
		if request.POST["button"] == "Play Cards" and player_object.phase != 2:
			## Make sure that no card is played twice
			valid = True
			for key in request.POST.keys():
				if "select" in key:
					for key_two in request.POST.keys():
						if request.POST[key_two] == request.POST[key]:
							if key_two != key:
								valid = False
						
			## and make sure no six is played where it shouldn't be
			sixes_error = False
			for province in game.province_set.all():
				card = Card.objects.get(pk=request.POST[province.name+"-select"])
				if card.card_value == "6":
					if player_one and province.player_one_played_six:
						valid = False
						sixes_error = True
						print(card, province)
					elif not player_one and province.player_two_played_six:
						valid = False
						sixes_error = True
						print(card, province)
							
			context["valid"] = valid
			context["sixes_error"] = sixes_error
			## check if player has already moved this turn
			moved = False
			if player_object.turns_taken == game.turn:
				moved = True
			
			if valid and not moved:
			
				## play card to province
				for province in game.province_set.all():
					card = Card.objects.get(pk=request.POST[province.name+"-select"])
					if player_one:
						province.player_one_card = card.card_value
					else:
						province.player_two_card = card.card_value
					
					## check if a player has played a 1
					if card.card_value == "1":
						player_object.played_one = True
													
					province.save()
					
					## if card is single-use, remove
					## need to decriment card_number to show we removed a card
					if card.is_single_use:
						player_object.card_number -= 1
						card.player.save()
						card.delete()
					
				## update the turns the player has taken
				player_object.turns_taken += 1
				player_object.phase = 1
				player_object.save()
				if player_one:
					player_one_obj = player_object
				else:
					player_two_obj = player_object

				print(player_object.id, player_one_obj.id, player_two_obj.id)
				print(game.turn, player_one_obj.turns_taken, player_two_obj.turns_taken, player_object.turns_taken)
				
				## Check if both players have made their move
				if player_two_obj.phase == 1 and player_one_obj.phase == 1:
	
					## add up the armies
					for province in game.province_set.all():
						province.add_armies()
						province.player_one_last_card = province.player_one_card
						province.player_two_last_card = province.player_two_card
						
						## only allowed to play a 6 on a given province once a game
						if province.player_one_card == "6":
							province.player_one_played_six = True
						if province.player_two_card == "6":
							province.player_two_played_six = True
						
						province.save()
					
					
					if game.turn % 3 == 0:
						## add up score
						round_score = 0
						round = game.turn / 3
						for province in game.province_set.all():
							armies = province.armies
							if round == 1:
								if armies > 0:
									round_score += province.round_one_points
								elif armies < 0:
									round_score -= province.round_one_points
							elif round == 2:
								if armies > 0:
									round_score += province.round_two_points
								elif armies < 0:
									round_score -= province.round_two_points
							else:
								if armies > 0:
									round_score += province.round_two_points
								elif armies < 0:
									round_score -= province.round_two_points
						game.score += round_score
						
						## determine if someone won
						if game.score > 8:
							game.winner = game.player_one
							game.over = True
						elif game.score < -8:
							game.winner = game.player_two
							game.over = True
						elif game.turn == 9:
							if game.score > 0:
								game.winner = game.player_one
							elif game.score < 0:
								game.winner = game.player_two
							game.over = True
					
					game.turn += 1
					game.save()
					
					## update players so that they can pick cards
					for player in [player_one_obj, player_two_obj, player_object]:
						player.phase = 2
						player.save()
				
		elif request.POST["button"] == "Pick Cards":		

		
		
			## give players new cards, first must check if selected right amount
			new_cards = []
			for key in request.POST.keys():
				if "select" in key:
					card = Card.objects.get(pk=request.POST[key])
					new_cards.append(card)
			print("new_cards", new_cards)
			
			## must select 2/3 or 1/2
			valid = False
			if player_object.played_one:
				valid = len(new_cards) == 2
				if len(player_object.next_cards()) == 1:
					valid = len(new_cards) == 1
			else:
				valid = len(new_cards) == 1
			if len(player_object.next_cards()) == 0:
				valid = True
			
			if valid and player_object.phase == 2:
				
				## card that doesn't get picked gets sent to the back
				card_options = player_object.next_cards()
				for card in card_options:
					if card not in new_cards:
						print("card not pickd", card.card_value, card.id)
						card.deck_position = 1 + len(player_object.see_cards())
						card.save()
				
				## update player_object to reflect adding cards to the hand
				player_object.card_number += len(new_cards)
				player_object.phase = 0
				player_object.save()
				
				
		print(game.turn, player_one_obj.turns_taken, player_two_obj.turns_taken, player_object.turns_taken)
	# print(player_one_obj.phase, player_two_obj.phase, player_object.phase)
		
	context["player_one_obj"] = player_one_obj
	context["player_two_obj"] = player_two_obj
	context["over"] = game.over
	
	
	return render(request, 'sun_tzu/game.html', context=context)


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))
	
	
def register(request):
	
	registered = False
	
	if request.method == "POST":
		user_form = UserForm(data=request.POST)
		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = UserProfileInfo(user=user)
			profile.save()

			registered = True
		else:
			print(user_form.errors)
	else:
		user_form = UserForm()
	return render(request, 'sun_tzu/registration.html', {"user_form":user_form, "registered":registered})
	
	
def user_login(request):
	
	if request.method == 'POST':
		username = request.POST.get('username') #*
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("ACCOUNT NOT ACTIVE")
		else:
			print("someone tried to login and failed")
			print(username, password)
			return HttpResponse("invalid login details supplied")
	else:
		return render(request, 'sun_tzu/login.html', {})
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	