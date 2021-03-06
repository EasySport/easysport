# URLconf
from django.urls import path

from . import views

app_name = 'lp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('donate/thanks', views.DonateThanksView.as_view(), name='donate_thanks'),
]
