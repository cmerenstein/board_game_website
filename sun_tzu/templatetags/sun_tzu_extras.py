from django import template

register = template.Library()

@register.filter
def get_next_cards(player, n):
	return player.next_cards(n)