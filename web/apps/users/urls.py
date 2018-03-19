from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path('reg/', views.RegistrationView.as_view(), name='signup'),
]
