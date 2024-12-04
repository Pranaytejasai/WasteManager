from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('register_user/', views.RegisterView, name="register_user"),
    path('login_user/', CustomLoginView.as_view(template_name='login.html'), name='login_user'),
    path('logout_user/', views.LogoutView, name='logout_user'),

]


