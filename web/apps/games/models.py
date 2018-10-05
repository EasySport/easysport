# Core django
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Our apps
from apps.courts.models import Court
from apps.sports.models import GameType


class Game(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    visibility = models.BooleanField(verbose_name='Публичная игра', default=True)
    is_reported = models.BooleanField(verbose_name='Создан отчет', default=False)

    # TODO: rename to responsible after migration
    responsible_user = models.ForeignKey(
        'users.User',
        verbose_name=u'Ответственный',
        related_name=u'responsible_user',
        on_delete=models.CASCADE
    )

    coach = models.ForeignKey(
        'users.User',
        null=True,
        blank=True,
        verbose_name=u'Тренер',
        related_name=u'coach',
        on_delete=models.CASCADE
    )

    capacity = models.SmallIntegerField(
        verbose_name='Вместимость',
        blank=True,
        default=0
    )

    # TODO: rename to reserved after migration
    reserved_count = models.PositiveIntegerField(
        verbose_name='Резервных мест',
        default=0
    )

    cost = models.SmallIntegerField(
        verbose_name='Цена',
        blank=True,
        default=0
    )

    court = models.ForeignKey(
        Court,
        verbose_name='Площадка',
        on_delete=models.CASCADE
    )

    gametype = models.ForeignKey(
        GameType,
        verbose_name='Тип игры',
        on_delete=models.CASCADE
    )

    datetime = models.DateTimeField(verbose_name='Начало')

    duration = models.DurationField(
        verbose_name=u'Длительность',
        help_text=u'В минутах',
        null=True,
        blank=True
    )

    # TODO: remove after migration
    description = models.CharField(max_length=300, verbose_name='Описание', blank=True, null=True)
    is_public = models.BooleanField('Публичный статус', default=True,
                                    help_text="Делает видимым в потоке")
    created_by = models.ForeignKey('users.User', blank=True, null=True, on_delete=models.CASCADE, related_name=u'created_by',)
    sporttype = models.ForeignKey('sports.SportType', verbose_name='Вид спорта', blank=True, null=True,
                                  on_delete=models.CASCADE)
    datetime_to = models.DateTimeField(verbose_name='Дата окончания', blank=True, auto_now=True)
    deleted = models.BooleanField(default=False, verbose_name='Игра удалена')

    class Meta:
        verbose_name = 'игра'
        verbose_name_plural = 'игры'

    def __str__(self):
        return u'{}, {}'.format(self.title, self.datetime)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('games:detail', args=[str(self.pk)])

    def delete(self, *args, **kwargs):
        # TODO: change to mass_mailing
        for usergameaction in self.subscribed_list():
            usergameaction.action = UserGameAction.UNSUBSCRIBED
            html_message = render_to_string(
                'mailing/build/delete_game_notification.html',
                {'game': self, 'user': usergameaction.user}
            )
            plain_message = strip_tags(html_message)

            send_mail(
                'Subject here',
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [usergameaction.user.email],
                fail_silently=True,
                html_message=html_message
            )
        super().delete(*args, **kwargs)

    def time_status(self):
        datetime = timezone.localtime(self.datetime)
        now = timezone.localtime(timezone.now())
        try:
            duration = timezone.timedelta(minutes=self.duration.seconds)
        except AttributeError:
            return 'Was'

        # Возвращаем list из флага, указывающего на то, что игра еще не прошла и статуса
        if now < datetime - duration:
            today = now.date()
            tomorrow = today + timezone.timedelta(days=1)
            double_tomorrow = today + timezone.timedelta(days=2)

            if datetime.date() == today and now < self.datetime:
                return 'Today'
            elif datetime.date() == tomorrow:
                return 'Tomorrow'
            elif datetime.date() == double_tomorrow:
                return 'After Tomorrow'
            else:
                return 'Will be'
        else:
            if now <= self.datetime:
                return 'Coming'
            elif now <= self.datetime + duration:
                return 'Goes'
            else:
                return 'Was'

    def need_report(self):
        if not self.is_reported and self.time_status() == 'Was':
            return True
        else:
            return False

    def subscribed_count(self):
        return UserGameAction.objects.filter(game=self).filter(status=UserGameAction.SUBSCRIBED).count()

    def subscribed_list(self):
        return UserGameAction.objects.filter(game=self).filter(status=UserGameAction.SUBSCRIBED)

    # TODO: uncomment after migration
    # def reserved_count(self):
    #     return UserGameAction.objects.filter(game=self).filter(status=UserGameAction.RESERVED).count()

    def reserved_list(self):
        return UserGameAction.objects.filter(game=self).filter(status=UserGameAction.RESERVED)

    def visited_count(self):
        return UserGameAction.objects.filter(game=self).filter(status=UserGameAction.VISITED).count()

    def visited_list(self):
        return UserGameAction.objects.filter(game=self).filter(status=UserGameAction.VISITED)


class UserGameAction(models.Model):
    class Meta:
        verbose_name = 'запись на игру'
        verbose_name_plural = 'записи на игру'
        unique_together = ("game", "user")

    SUBSCRIBED = 1
    RESERVED = 2
    UNSUBSCRIBED = 3
    VISITED = 4
    NOTVISITED = 5
    STATUSES = (
        (SUBSCRIBED, 'Записался'),
        (UNSUBSCRIBED, 'Отписался'),
        (RESERVED, 'В резерве'),
        (VISITED, 'Посетил'),
        (NOTVISITED, 'Не пришел')
    )

    _SUBSCRIBED = 1
    _UNSUBSCRIBED = 2
    _RESERVED = 3
    _UNRESERVED = 4
    _VISITED = 5
    _NOTVISITED = 6
    _NOTPAY = 7
    ACTIONS = (
        (_SUBSCRIBED, 'Записался'),
        (_UNSUBSCRIBED, 'Отписался'),
        (_RESERVED, 'В резерве'),
        (_UNRESERVED, 'Вышел из резерва'),
        (_VISITED, 'Посетил'),
        (_NOTVISITED, 'Не пришел'),
        (_NOTPAY, 'Не заплатил')
    )

    user = models.ForeignKey(
        'users.User',
        verbose_name='Пользователь',
        related_name=u'usergameaction',
        on_delete=models.CASCADE
    )

    game = models.ForeignKey(
        Game,
        verbose_name='Игра',
        on_delete=models.CASCADE
    )

    datetime = models.DateTimeField(verbose_name='Дата действия', auto_now=True)

    # TODO: rename action to status after migration and reload action to statuses
    status = models.PositiveSmallIntegerField(verbose_name='Действие', choices=STATUSES, null=True)
    action = models.PositiveSmallIntegerField(verbose_name='Action (old)', choices=ACTIONS, null=True)

    def __str__(self):
        return u'{} {} | {} | {}'.format(self.game.id, self.game, self.user, self.get_status_display())
