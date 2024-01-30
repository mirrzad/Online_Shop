from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
    path('activate-account/<email_activation_code>/', views.ActivationView.as_view(), name='activate-account'),
    path('forgot-password', views.ForgotPassword.as_view(), name='forgot_password'),
    path('reset-password/<active_code>', views.ResetPassword.as_view(), name='reset_password')
]
