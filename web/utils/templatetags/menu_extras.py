# Inside custom tag - is_active.py
from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def is_active(request, url):
    try:
        path = request.path
        # Main idea is to check if the url and the current path is a match
        if path == reverse(url):
            return "active"
        return ""
    except AttributeError:
        return ""
