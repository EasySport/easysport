# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    'apps.users.backends.EmailBackend',
)

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = 'users:login'
LOGOUT_REDIRECT_URL = 'lp:index'
LOGIN_REDIRECT_URL = 'lp:index'

SOCIAL_AUTH_FACEBOOK_KEY = '566580510366604'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '9d22ec108abfaff23f47a4c0fb77c095'  # App Secret
