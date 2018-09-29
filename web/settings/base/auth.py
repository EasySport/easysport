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
    'social_core.backends.vk.VKOAuth2',

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    'apps.users.backends.EmailBackend',
)

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = 'users:login'
LOGOUT_REDIRECT_URL = 'lp:index'
LOGIN_REDIRECT_URL = 'lp:index'


# Social auth http://python-social-auth.readthedocs.io/en/latest/backends/vk.html

SOCIAL_AUTH_FACEBOOK_KEY = '566580510366604'
SOCIAL_AUTH_FACEBOOK_SECRET = '9d22ec108abfaff23f47a4c0fb77c095'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'ru_RU',
  'fields': 'id,email,first_name,gender,last_name,profile_pic,birthday'
}

SOCIAL_AUTH_VK_OAUTH2_KEY = '6449434'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'YEB21MbBeWL2y6hqp5Gd'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = ['first_name', 'last_name', 'photo_200_orig', 'sex', 'bdate',
                                    'city', 'country', 'has_photo', 'has_mobile', 'contacts', 'screen_name']

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.mail.mail_validation',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_LOGIN_ERROR_URL = '/profile/update/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/games'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/profile/update/?next=/games&new_user=1'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

SOCIAL_AUTH_REDIRECT_IS_HTTPS = False
