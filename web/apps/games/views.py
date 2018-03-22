# Django core
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils import timezone

# Third party
from dal import autocomplete

# Our apps
from .models import Game
from apps.sports.models import SportType


class GamesList(ListView):
    model = Game

    def get_queryset(self, **kwargs):
        sport = self.request.GET.get('sport', None)
        q = Game.objects.filter(datetime__gte=timezone.now())
        if sport:
            return q.filter(gametype=sport)
        return q

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GamesList, self).get_context_data(**kwargs)
        context['sports'] = SportType.objects.all()
        return context


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
        initial['datetime'] = timezone.now()
        return initial

    def get_form(self, form_class=None):
        form = super(GameCreate, self).get_form(form_class)
        form.fields['court'].widget = autocomplete.ModelSelect2(url='courts:autocomplete')
        form.fields['court'].widget.choices = form.fields['court'].choices
        return form


class GameUpdate(UpdateView):
    model = Game
    fields = '__all__'
    permission_required = 'games.can_edit'
    template_name = 'games/game_edit.html'

    def get_form(self, form_class=None):
        form = super(GameUpdate, self).get_form(form_class)
        form.fields['court'].widget = autocomplete.ModelSelect2(url='courts:autocomplete')
        form.fields['court'].widget.choices = form.fields['court'].choices
        return form
