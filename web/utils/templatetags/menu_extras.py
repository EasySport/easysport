# Inside custom tag - is_active.py
from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def is_active(request, url):
    # Main idea is to check if the url and the current path is a match
    if request.path == reverse(url):
        return "active"
    return ""


@register.inclusion_tag('particles/city_nav.html', takes_context=True)
def city_nav(context):
    request = context['request']
    user = request.user
    new_context = {
        'user': user
    }
    return new_context
