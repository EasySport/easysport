# Django core
import json
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.shortcuts import render, HttpResponse

# Third party
from dal import autocomplete

# Our apps
from .models import Game, UserGameAction
from apps.sports.models import SportType
from apps.users.models import User
from apps.courts.models import Court

from utils.templatetags.user_extras import can_see_game


class GamesList(ListView):
    model = Game

    def get_queryset(self, **kwargs):
        games = Game.objects.filter(datetime__gte=timezone.now()).order_by('datetime')

        # Hide private games
        if not can_see_game(self.request.user):
            games = games.filter(visibility=True)

        # Show games only from user's city
        if self.request.user.is_authenticated and self.request.user.city:
            games = games.filter(court__place__city=self.request.user.city)
        else:
            # If User.city is None
            # TODO: No template names provided fix (redirect('users:update'))
            # return redirect('users:update')
            pass

        sport = self.request.GET.get('sport', None)
        if sport and sport != 'all':
            games = games.filter(gametype=sport)
        return games

    def get_context_data(self, *, object_list=None, **kwargs):
        sport = self.request.GET.get('sport', None)
        context = super(GamesList, self).get_context_data(**kwargs)
        context['sports'] = SportType.objects.all()
        if sport and sport != 'all':
            context['q'] = int(sport)
        return context


class GameDetail(DetailView):
    model = Game
    context_object_name = 'game'


class GameCreate(PermissionRequiredMixin, CreateView):
    model = Game
    permission_required = 'games.can_create'

    fields = ('title', 'visibility', 'responsible',
              'coach', 'gametype', 'capacity', 'reserved',
              'court', 'datetime', 'duration', 'cost')

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
    permission_required = 'games.can_edit'
    template_name = 'games/game_edit.html'

    fields = ('title', 'visibility', 'responsible',
              'coach', 'gametype', 'capacity', 'reserved',
              'court', 'datetime', 'duration', 'cost')


    def get_form(self, form_class=None):
        form = super(GameUpdate, self).get_form(form_class)
        form.fields['court'].widget = autocomplete.ModelSelect2(url='courts:autocomplete')
        form.fields['court'].widget.choices = form.fields['court'].choices
        return form


# Return error for ajax
def error_response(description):
    error = {'error_description': description}
    return HttpResponse(json.dumps({'error': error}), content_type="application/json")


@require_POST
def game_action(request):
    if request.is_ajax():
        status = request.POST["action"]
        game_id = request.POST["game_id"]
        if request.user.is_authenticated:
            user = User.objects.get(email=request.user.email)
            game = Game.objects.get(id=game_id)

            if status == '1':
                set_status = UserGameAction.SUBSCRIBED
            elif status == '3':
                set_status = UserGameAction.UNSUBSCRIBED
            elif status == '2':
                set_status = UserGameAction.RESERVED

            try:
                user_game_action = UserGameAction.objects.get(game=game, user=user)
                current_status = user_game_action.status
                if current_status == set_status:
                    return error_response('Action already save')
                else:
                    # TODO: add check of game in similar time
                    if set_status == UserGameAction.SUBSCRIBED and not (game.capacity > game.subscribed_count()):
                        return error_response('There is no place now')
                    elif set_status == UserGameAction.RESERVED and not (game.reserved > game.reserved_count()):
                        return error_response('There is no place now')
                    user_game_action.status = set_status
                    user_game_action.save()
                    return render(request, 'games/game_card.html', {'game': game, 'user': user})
            except UserGameAction.DoesNotExist:
                UserGameAction.objects.create(game=game, user=user, status=set_status)
                # TODO: email user
                return render(request, 'games/game_card.html', {'game': game, 'user': user})
        else:
            return error_response('Not auth')
    else:
        return error_response('Not AJAX')


def get_recommended_price(request):
    price = 0
    params = request.GET

    try:
        court = int(params.get('court', ''))
        duration = int(params.get('duration', ''))
        game_capacity = int(params.get('game_capacity', ''))

        c = Court.objects.get(pk=court)
    except Court.DoesNotExist:
        error_response('Court does not exists')
    except (ValueError, ZeroDivisionError):
        pass
    else:
        price = (c.price * (duration / 60)) * 1.3 / game_capacity

    return HttpResponse(round(price / 10) * 10)
