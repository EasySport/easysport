# Inside custom tag - is_active.py
from django import template
from utils import formatters

register = template.Library()


@register.filter
def in_minutes(td):
    minutes = td.seconds
    if minutes % 30 == 0:
        hours = minutes/60
        if minutes % 60 == 0:
            hours = int(hours)
        return formatters.show_hours(hours)
    else:
        return formatters.show_minutes(minutes)
