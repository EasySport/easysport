# Core django
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')

    # creator = models.ForeignKey('users.User', blank=True, null=True)
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

    # court = models.ForeignKey(Court, verbose_name='Площадка')

    # gametype = models.ForeignKey(GameType, verbose_name='Тип игры')
    # sporttype = models.ForeignKey(SportType, verbose_name='Вид спорта', blank=True, null=True)

    datetime = models.DateTimeField(verbose_name='Дата проведения')
    duration = models.DurationField(
        verbose_name=u'Длительность',
        help_text=u'В минутах',
        null=True,
        blank=True
    )

    class Meta():
        verbose_name = 'игра'
        verbose_name_plural = 'игры'

    def __str__(self):
        return u'Игра #{}'.format(self.id)
