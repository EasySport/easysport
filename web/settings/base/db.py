import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': int(os.getenv('POSTGRES_PORT')),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD')
    }
}
