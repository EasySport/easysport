import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

# Сюда упадут все файлы на production после collectstatic
# Важно не использовать STATICFILES_FINDERS на production, а например nginx
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# В этих директориях django ищет статические файлы.
# Если не находит, то ищет с помощью django.contrib.staticfiles.finders.AppDirectoriesFinder,
# которая проверяет папку static каждого установленного в проекте приложения
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

# В режиме разработки — python manage.py runserver — Django ищет статичные файлы с помощью них
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Сюда упадут все файлы загруженные динамически
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = '/media/'