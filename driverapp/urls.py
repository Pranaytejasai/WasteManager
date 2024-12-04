from django.urls import path
from . import views
from .views import view_driver_details

app_name = 'driverapp'

urlpatterns = [
    path('profile/', views.driver_profile, name='profile'),
    path('dashboard/', views.driver_dashboard, name='dashboard'),
    path('details/<int:driver_id>/', view_driver_details, name='view_driver_details'),
    path('dashboard/', views.driver_dashboard, name='dashboard'),
    path('send_email/<int:user_id>/', views.send_email, name='send_email')

]
