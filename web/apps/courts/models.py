# Django core
from django.db import models
from django.contrib.postgres.fields import JSONField

# Third party
import geocoder


class Country(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)

    class Meta():
        verbose_name = 'страна'
        verbose_name_plural = 'страны'

    def __str__(self):
        return self.title


class City(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название',
        unique=True
    )

    country = models.ForeignKey(
        Country,
        verbose_name='Страна',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'

    def __str__(self):
        return self.title


class Place(models.Model):
    city = models.ForeignKey(
        City,
        verbose_name='Город',
        on_delete=models.CASCADE
    )

    longitude = models.FloatField(
        verbose_name='Долгота',
        help_text='Возьмите из Яндекс карт',
        blank=True,
        null=True
    )

    latitude = models.FloatField(
        verbose_name='Широта',
        help_text='Возьмите из Яндекс карт',
        blank=True,
        null=True
    )

    address = models.CharField(
        max_length=500,
        verbose_name='Адрес',
        unique=True,
        help_text='В формате "ул. Московская, д.9"'
    )

    geo_json = JSONField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'

    def __str__(self):
        return self.address

    def save(self, *args, **kwargs):
        # http://geocoder.readthedocs.io
        g = geocoder.yandex(u'{} {}'.format(self.city, self.address), lang='ru_RU')
        geo_json = g.geojson
        self.geo_json = geo_json
        self.address = geo_json['features'][0]['properties']['address']
        self.longitude = geo_json['features'][0]['properties']['lng']
        self.latitude = geo_json['features'][0]['properties']['lat']
        super().save(*args, **kwargs)


class CourtType(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название типа площадки'
    )

    class Meta:
        verbose_name = 'тип площадки'
        verbose_name_plural = 'типы площадок'

    def __str__(self):
        return self.title


# Define where to store image
# Instance is an instanсe of model, that contains image
def court_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/...
    return 'courts/{0}/{1}/{2}'.format(
        instance.place.city,
        instance.title,
        filename)


# Court model is separated from place for dealing with multiple courts in one place
class Court(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True
    )

    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        help_text='Это описание увидят все посетители сайта'
    )

    admin_description = models.TextField(
        verbose_name='Примечания для админов',
        blank=True,
        help_text='Это описание только для организаторов игр'
    )

    place = models.ForeignKey(
        Place,
        verbose_name='Место',
        on_delete=models.CASCADE
    )

    type = models.ForeignKey(
        CourtType,
        verbose_name='Тип площадки',
        on_delete=models.CASCADE
    )

    photo = models.ImageField(
        upload_to=court_image_directory_path,
        verbose_name='Фотография зала',
        blank=True
    )

    views = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'площадка'
        verbose_name_plural = 'площадки'
        ordering = ['-views']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('courts:detail', args=[str(self.pk)])
