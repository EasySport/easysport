# Django core
from django.views.generic import ListView, DetailView

# Our apps
from .models import Game


class GamesList(ListView):
    model = Game


class GameDetail(DetailView):
    model = Game
