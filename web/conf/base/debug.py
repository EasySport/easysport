MIDDLEWARE += [
   'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INSTALLED_APPS += (
   'debug_toolbar',
)

DEBUG_TOOLBAR_PANELS = [
   'debug_toolbar.panels.versions.VersionsPanel',
   'debug_toolbar.panels.timer.TimerPanel',
   'debug_toolbar.panels.settings.SettingsPanel',
   'debug_toolbar.panels.headers.HeadersPanel',
   'debug_toolbar.panels.request.RequestPanel',
   'debug_toolbar.panels.sql.SQLPanel',
   'debug_toolbar.panels.staticfiles.StaticFilesPanel',
   'debug_toolbar.panels.templates.TemplatesPanel',
   'debug_toolbar.panels.cache.CachePanel',
   'debug_toolbar.panels.signals.SignalsPanel',
   'debug_toolbar.panels.logging.LoggingPanel',
   'debug_toolbar.panels.redirects.RedirectsPanel',
]

def show_toolbar(request):
    if request.user.is_staff:
        return True
    return False

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar
}