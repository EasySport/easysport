from django.urls import path
import django.contrib.auth.views as auth_views

from . import views

app_name = 'users'

urlpatterns = [
    path('reg/', views.RegistrationView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password/reset/', views.ResetView.as_view(), name='password_reset'),
    path('password/reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password/password_reset_done.html'),
         name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/',
         views.ResetConfirmView.as_view(post_reset_login=True), name='password_reset_confirm'),

    path('users/', views.UsersList.as_view(), name='list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='detail'),
    path('profile/update/', views.ProfileUpdate.as_view(), name='update'),
    path('profile/password/', views.password, name='password'),
]
