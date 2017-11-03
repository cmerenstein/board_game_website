from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from sun_tzu.forms import UserForm, GameForm
from .models import Game, Province, UserProfileInfo
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
	if request.method == "POST":
		game_form = GameForm(data=request.POST)
		
		if game_form.is_valid():
			game = game_form.save()
			for province in PROVINCES:
				r_one = random.randint(1,5)
				r_two = random.randint(1,5)
				r_three = random.randint(1,5)
				game.province_set.create(name=province, round_one_points=r_one, round_two_points=r_two, round_three_points=r_three)
								
			game.save()
			return HttpResponseRedirect(reverse('sun_tzu:game_view', kwargs={'game_id': game.game_id}))
	
	else:
		game_form = GameForm()
		
	return render(request, 'sun_tzu/new_game.html', {"form":game_form})

@login_required	
def game_view(request, game_id):
	game = get_object_or_404(Game, pk=game_id)

	player_logged_in = False
	if request.user == game.player_one.user or request.user == game.player_two.user:
		player_logged_in = True

	return render(request, 'sun_tzu/game.html', {"game":game, "player_logged_in":player_logged_in, "player": request.user})

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/sun_tzu/user_login/'
	return HttpResponse("You are logged in. User is " + str(request.user))	
	
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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	