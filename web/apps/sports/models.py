from django.db import models


class SportType(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название вида спорта'
    )

    class Meta:
        verbose_name = 'Вид спорта'
        verbose_name_plural = 'Виды спорта'

    def __str__(self):
        return self.title


class GameType(models.Model):
    sport_type = models.ForeignKey(
        SportType,
        verbose_name='Вид спорта',
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=100,
        verbose_name='Название типа игры'
    )

    description = models.TextField(
        verbose_name='Описание формата',
        blank=True
    )

    class Meta:
        verbose_name = 'Тип игры'
        verbose_name_plural = 'Типы игры'

    def __str__(self):
        return u'{} - {}'.format(self.sport_type.title, self.title)


class Amplua(models.Model):
    sport_type = models.ForeignKey(
        SportType,
        verbose_name='Вид спорта',
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'амплуа'
        verbose_name_plural = 'амплуа'

    def __str__(self):
        return u'{} - {}'.format(self.sport_type.title, self.title)
