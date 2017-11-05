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

@login_required
def new_game(request):
	PROVINCES = ["Wu", "Han-Qi", "Jin-Yan", "Chu", "Qin"]
	BASE_CARDS = ["1", "2", "3", "4", "5", "6"]
	EXTRA_CARDS = ["+1", "+1", "+1", "-1", "-1", "-1", "P", "P", "P", "7", "8", "9", "10"]
	
	if request.method == "POST":
		game_form = GameForm(data=request.POST)
		
		if game_form.is_valid():
			game = game_form.save()
			
			### give provinces values
			for province in PROVINCES: 
				r_one = random.randint(1,5)
				r_two = random.randint(1,5)
				r_three = random.randint(1,5)
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
				p.card_number = 10 ## to start the player takes 10 cards
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
	context["player_one_obj"] = player_one_obj
	player_two_obj = game.player_set.get(player_name=game.player_two.user.username)	
	context["player_two_obj"] = player_two_obj
	
	if request.method == "POST":
		
		### Make sure that no card is played twice
		valid = True
		for key in request.POST.keys():
			if "select" in key:
				for key_two in request.POST.keys():
					if request.POST[key_two] == request.POST[key]:
						if key_two != key:
							valid = False
		context["valid"] = valid
		
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
				province.save()
				
				## if card is single-use, remove
				if card.is_single_use:
					card.delete()
				
			## update the turns the player has taken	
			if player_one:
				player_one_obj.turns_taken += 1
				player_one_obj.save()
			else:
				player_two_obj.turns_taken += 1
				player_two_obj.save()

			print(player_object.id, player_one_obj.id, player_two_obj.id)
			print(game.turn, player_one_obj.turns_taken, player_two_obj.turns_taken, player_object.turns_taken)
			
			## Check if both players have made their move
			if player_one_obj.turns_taken == game.turn and player_two_obj.turns_taken == game.turn:
				## add up the armies
				for province in game.province_set.all():
					province.add_armies()
					province.save()
				game.turn += 1
				game.save()
				
				
		print(game.turn, player_one_obj.turns_taken, player_two_obj.turns_taken, player_object.turns_taken)	
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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	