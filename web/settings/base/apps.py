INSTALLED_APPS = [
    # Autocomplete
    'dal',
    'dal_select2',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # External libraries
    # - Bootstrap
    'bootstrap4',
    # - Models
    'phonenumber_field',
    # - Social authorization
    'social_django',

    'extra_views',

    # Our apps
    'apps.courts',
    'apps.games',
    'apps.lp',
    'apps.mailing',
    'apps.sports',
    'apps.users',

    # Utils like filters etc
    'utils',
]
