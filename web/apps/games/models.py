# Core django
from django.db import models
from django.utils import timezone

# Our apps
from apps.courts.models import Court
from apps.sports.models import GameType
from apps.users.models import User


class Game(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    visibility = models.BooleanField(verbose_name='Публичная игра', default=True)
    is_reported = models.BooleanField(verbose_name='Создан отчет', default=False)

    responsible = models.ForeignKey(
        User,
        verbose_name=u'Ответственный',
        related_name=u'responsible',
        on_delete=models.CASCADE
    )

    coach = models.ForeignKey(
        User,
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

    reserved = models.PositiveIntegerField(
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

    class Meta:
        verbose_name = 'игра'
        verbose_name_plural = 'игры'

    def __str__(self):
        return u'{}, {}'.format(self.title, self.datetime)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('games:detail', args=[str(self.pk)])

    @property
    def time_status(self):
        event_date = timezone.localtime(self.datetime).date()
        now = timezone.localtime(timezone.now())
        duration = self.duration
        today = now.date()
        tomorrow = today + timezone.timedelta(days=1)
        double_tomorrow = today + timezone.timedelta(days=2)

        # Возвращаем list из флага, указывающего на то, что игра еще не прошла и статуса
        if now < self.datetime - duration:
            if event_date == today and now < self.datetime:
                return 'Today'
            elif event_date == tomorrow:
                return 'Tomorrow'
            elif event_date == double_tomorrow:
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

    def subscribed_count(self):
        return UserGameAction.objects.filter(game=self).filter(status=UserGameAction.SUBSCRIBED).count()

    def subscribed_list(self):
        return UserGameAction.objects.filter(game=self).filter(status=UserGameAction.SUBSCRIBED)

    def reserved_count(self):
        return UserGameAction.objects.filter(game=self).filter(status=UserGameAction.RESERVED).count()

    def reserved_list(self):
        return UserGameAction.objects.filter(game=self).filter(status=UserGameAction.RESERVED)


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

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )

    game = models.ForeignKey(
        Game,
        verbose_name='Игра',
        on_delete=models.CASCADE
    )

    datetime = models.DateTimeField(verbose_name='Дата действия', auto_now=True)

    status = models.PositiveSmallIntegerField(verbose_name='Действие', choices=STATUSES)

    def __str__(self):
        return u'{} {} | {} | {}'.format(self.game.id, self.game, self.user, self.get_status_display())
