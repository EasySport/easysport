# URLconf
from django.urls import path

from . import views


app_name = 'games'

urlpatterns = [
    path('', views.GamesList.as_view(), name='list'),
    path('<int:pk>/', views.GameDetail.as_view(), name='detail'),
]