from django.conf import settings


class EmailBackend:
    """
    Authenticate with email and password
    """
    def authenticate(self, request, email=None, password=None):
        try:
            user = settings.AUTH_USER_MODEL.objects.get(email=email)
        except settings.AUTH_USER_MODEL.DoesNotExist:
            # Create a new user. There's no need to set a password
            # because only the password from settings.py is checked.
            user = settings.AUTH_USER_MODEL(email=email)
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return settings.AUTH_USER_MODEL.objects.get(pk=user_id)
        except settings.AUTH_USER_MODEL.DoesNotExist:
            return None
