# Django core
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

# Our apps
from .models import Game


class GamesList(ListView):
    model = Game


class GameDetail(DetailView):
    model = Game


class GameCreate(CreateView):
    model = Game
    fields = '__all__'

    def get_initial(self):
        initial = super(GameCreate, self).get_initial()
        initial = initial.copy()
        initial['responsible'] = self.request.user
        return initial
