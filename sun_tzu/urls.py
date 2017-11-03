from django.conf.urls import url
from . import views

app_name = 'sun_tzu'
urlpatterns = [
	url(r'^register/$', views.register, name='register'),
	url(r'^user_login/$', views.user_login, name='user_login'),
	url(r'^new_game/$', views.new_game, name="new_game"),
	url(r'^(?P<game_id>[0-9]+)/$', views.game_view, name="game_view"),
]
