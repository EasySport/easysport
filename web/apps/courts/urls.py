# URLconf
from django.urls import path

from . import views


app_name = 'courts'

urlpatterns = [
    path('', views.CourtsList.as_view(), name='list'),
    path('<int:pk>/', views.CourtDetail.as_view(), name='detail'),

    path('create/place/', views.PlaceCreate.as_view(), name='create_place'),
    path('create/', views.CourtCreate.as_view(), name='create'),
    path('<int:pk>/update/', views.CourtUpdate.as_view(), name='update'),

    path('autocomplete/', views.CourtAutocomplete.as_view(), name='autocomplete'),
]
