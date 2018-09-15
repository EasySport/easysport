import json
from datetime import timedelta

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib import messages

from django.db.models import F, Q
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse

from django.utils import timezone
from django.utils.decorators import method_decorator

from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from dal import autocomplete
from extra_views import ModelFormSetView

from apps.courts.models import Court
from apps.sports.models import SportType
from apps.users.models import User

from utils.templatetags.user_extras import can_see_game

from .models import Game, UserGameAction


class GamesList(ListView):
    model = Game

    # paginate_by = 15

    def get_queryset(self, **kwargs):
        games = Game.objects.filter(datetime__gte=timezone.now()).order_by('datetime')
        user = self.request.user

        # Hide private games
        if not can_see_game(user):
            games = games.filter(visibility=True)

        # Show games only from user's city
        if user.is_authenticated and user.city:
            games = games.filter(court__place__city=user.city)
        else:
            messages.error(self.request, 'Вы не указали свой город в профиле', extra_tags='city')

        sport = self.request.GET.get('sport', None)

        if sport:
            # Sort games by gametype
            if sport not in ['all', 'my', 'need_report']:
                games = games.filter(gametype=sport)

            # Show user's games
            if sport == 'my' and can_see_game(user):
                games = Game.objects.filter(responsible=user)

            # Show games waiting for a report
            if sport == 'need_report' and can_see_game(user):
                games = Game.objects.filter(
                    Q(is_reported=False)
                    & Q(responsible=user)
                    & Q(datetime__lte=timezone.now() - F('duration'))
                )

        return games

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GamesList, self).get_context_data(**kwargs)
        context['sports'] = SportType.objects.all()

        sport = self.request.GET.get('sport', None)

        if sport == 'need_report':
            context.update({'need_report': True})

        if sport and sport != 'all':
            context['q'] = sport
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


@method_decorator(permission_required('games.can_edit'), 'dispatch')
class GameReport(ModelFormSetView):
    model = UserGameAction
    fields = ('user', 'status')
    factory_kwargs = {'extra': 0}
    template_name = 'games/game_report.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        return super(GameReport, self).get_queryset().filter(game=pk)

    def get_success_url(self):
        return reverse('games:report_done', kwargs={'pk': self.kwargs['pk']})


@method_decorator(permission_required('games.can_edit'), 'dispatch')
class GameReportDone(UpdateView):
    model = Game
    context_object_name = 'game'
    fields = '__all__'
    template_name = 'games/game_report_done.html'

    def get_context_data(self, **kwargs):
        context = super(GameReportDone, self).get_context_data(**kwargs)
        game = context['game']

        # Current user is game's responsible and game isn't reported
        if game.responsible == self.request.user and not game.is_reported:
            game.is_reported = True
            game.save()

        return context


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

    if game_capacity == 0:
        pass
    else:
        price = (c.price * (duration / 60)) * 1.3 / game_capacity

    return HttpResponse(round(price / 10) * 10)


@method_decorator(permission_required('games.can_edit'), 'dispatch')
def copy_game(request, pk):
    game = Game.objects.get(pk=pk)
    new_date = game.datetime + timedelta(days=7)

    # Clone game and set date to next week
    game.pk = None
    game.datetime = new_date
    game.is_reported = False
    game.save()

    return redirect('games:update', game.pk)
