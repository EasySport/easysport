"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Development
import debug_toolbar
import django.contrib.auth.views as auth_views
# Django core
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    # Core django paths
    path('admin/', admin.site.urls),

    # Our apps
    path('games/', include('apps.games.urls')),
    path('courts/', include('apps.courts.urls')),
    path('', include('apps.lp.urls')),

    # Login views
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Development
    path('__debug__/', include(debug_toolbar.urls)),
]