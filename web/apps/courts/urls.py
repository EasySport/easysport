# URLconf
from django.urls import path

from . import views


app_name = 'courts'

urlpatterns = [
    path('', views.CourtsList.as_view(), name='list'),
    path('<int:pk>/', views.CourtDetail.as_view(), name='detail'),
]