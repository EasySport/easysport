import os

# Best place to change this env variables is project/settings/local/env.py file. It loads after this one specially to
# allow you manage env without touching project code.

if os.getenv('DJANGO_ENV') == 'production':
    DEBUG = False
    ALLOWED_HOSTS = ['dev.easysport.online', 'easysport.online']
    # ...
else:
    DEBUG = True
    ALLOWED_HOSTS = ['*']