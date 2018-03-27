# Inside custom tag - is_active.py
from django import template
from django.utils import timezone

from utils import formatters

register = template.Library()


@register.filter(name='beauty_age')
def beauty_age(value):
    today = timezone.now()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    return formatters.show_years(age)
