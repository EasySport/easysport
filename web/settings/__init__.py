import os
from split_settings.tools import include, optional

ENVIRONMENT = os.getenv('DJANGO_ENV') or 'development'

include(
    # Load environment settings
    'base/env.py',
    optional('local/env.py'),  # We can "patch" any settings from local folder env.py file.

    # Here we should have the order because of dependencies
    'base/paths.py',
    'base/apps.py',
    'base/middleware.py',

    # Load all other settings
    'base/*.py',

    # Select the right env:
    'environments/%s.py' % ENVIRONMENT,

    optional('local/*.py'),  # we can load any other settings from local folder
)