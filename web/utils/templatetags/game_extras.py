# Inside custom tag - is_active.py
from django import template

# Our apps
from apps.games.models import UserGameAction
from utils import formatters

register = template.Library()


@register.filter
def in_minutes(td):
    try:
        minutes = td.seconds
    except AttributeError:
        pass
    else:
        if minutes % 30 == 0:
            hours = minutes / 60
            if minutes % 60 == 0:
                hours = int(hours)
            return formatters.show_hours(hours)
        else:
            return formatters.show_minutes(minutes)


@register.inclusion_tag('games/game_card.html')
def game_card(game, user):
    new_context = {
        'game': game,
        'user': user
    }
    return new_context


@register.inclusion_tag('games/game_status_button.html')
def game_status_button(game, user):
    try:
        action = UserGameAction.objects.get(user=user, game=game)
    except UserGameAction.DoesNotExist:
        action = None
    except TypeError:
        action = None

    new_context = {
        'game': game,
        'action': action,
        'user': user
    }
    return new_context
