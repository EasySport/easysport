from django.urls import path

from . import views

app_name = 'games'

urlpatterns = [
    path('', views.GamesList.as_view(), name='list'),
    path('<int:pk>/', views.GameDetail.as_view(), name='detail'),
    path('<int:pk>/update/', views.GameUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', views.GameDelete.as_view(), name='delete'),
    path('<int:pk>/report/', views.GameReport.as_view(), name='report'),
    path('<int:pk>/report_done/', views.GameReportDone.as_view(), name='report_done'),
    path('<int:pk>/report_done/copy', views.copy_game, name='copy_game'),

    path('create/', views.GameCreate.as_view(), name='create'),

    path('action/', views.game_action, name='game_action'),
    path('get_recommended_price/', views.get_recommended_price, name='get_recommended_price')
]
