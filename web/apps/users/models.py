# Django core
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.urls import reverse

# Third party
from phonenumber_field.modelfields import PhoneNumberField

# Our apps
from apps.courts.models import City


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


def avatar_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/...
    return 'avatar/{0}/{1}'.format(
        instance.pk,
        filename)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email', unique=True)
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)
    is_active = models.BooleanField('Активный профиль', default=True)
    is_staff = models.BooleanField('Статус админа', default=False)

    city = models.ForeignKey(
        City,
        verbose_name='Город',
        on_delete=models.CASCADE,
        null=True
    )
    sex = models.CharField(max_length=1, choices=(('m', 'мужской'), ('f', 'женский')), verbose_name='Пол')
    bdate = models.DateField(
        'Дата рождения',
        auto_now_add=False,
        blank=True,
        null=True,
        help_text=u'В формате ДД.ММ.ГГГГ'
    )
    phone = PhoneNumberField(
        verbose_name='Мобильный телефон',
        unique=True,
        null=True,
        help_text=u'В формате +7**********'
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to=avatar_path,
        null=True,
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        if self.first_name != "" and self.last_name != "":
            return u'{} {}'.format(self.first_name, self.last_name)
        else:
            return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def get_absolute_url(self):
        return reverse('users:detail', args=[str(self.pk)])
