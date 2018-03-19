# Django core
from django.db import models


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
    return 'courts/{0}/{1}'.format(
        instance.title,
        filename)


class Court(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True
    )

    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )

    admin_description = models.TextField(
        verbose_name='Примечания для админов',
        blank=True
    )

    # place = models.ForeignKey(Place, verbose_name='Место')

    type = models.ForeignKey(
        CourtType,
        verbose_name='Тип площадки',
        on_delete=models.CASCADE
    )

    photo = models.ImageField(
        upload_to=court_image_directory_path,
        verbose_name='Изображение',
        blank=True
    )

    # sporttypes = models.ManyToManyField(SportType, verbose_name=u'Типы спорта', blank=True)

    views = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'площадка'
        verbose_name_plural = 'площадки'
        ordering = ['-views']

    def __str__(self):
        return self.title
