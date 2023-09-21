from django.urls import path

from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login', views.LoginInterfaceView.as_view(), name='login'),
    path('logout', views.LogoutInterfaceView.as_view(), name='logout'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('profile/change_email', views.ChangeEmailView.as_view(), name='change_email'),
    path('profile/change_password', views.ChangePasswordView.as_view(), name='change_password'),
    path('profile/password-reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('profile/password-reset-done/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('profile/password-reset-confirm/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/password-reset-complete/', views.MyPasswordResetCompleteView.as_view(),name='password_reset_complete'),
]