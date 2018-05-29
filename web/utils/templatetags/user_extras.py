# Inside custom tag - is_active.py
from django import template
from django.utils import timezone

from utils import formatters

register = template.Library()


def check_permissions(user, groups=None):
    if groups is None:
        groups = []
    groups.append('admin')

    visibility = False

    if user.groups.filter(name__in=groups).exists():
        visibility = True

    return visibility


@register.filter(name='beauty_age')
def beauty_age(value):
    today = timezone.now()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    return formatters.show_years(age)


@register.filter
def can_see_phone(user):
    return check_permissions(user, ['responsible'])


@register.filter
def can_see_game(user):
    return check_permissions(user, ['responsible'])
