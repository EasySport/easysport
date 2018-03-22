# Django core
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin

# Our apps
from .models import Game


class GamesList(ListView):
    model = Game


class GameDetail(DetailView):
    model = Game


class GameCreate(PermissionRequiredMixin, CreateView):
    model = Game
    fields = '__all__'
    permission_required = 'games.can_create'

    def get_initial(self):
        initial = super(GameCreate, self).get_initial()
        initial = initial.copy()
        initial['responsible'] = self.request.user
        return initial
