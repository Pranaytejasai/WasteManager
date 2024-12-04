from django.urls import path
from . import views

app_name = "profileapp"
urlpatterns = [
        path('profile/', views.user_profile, name='user_profile'),
        path('edit/', views.edit_profile, name='edit_profile'),
        path('add-address/', views.add_address, name='add_address'),
        path('profile/delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
        path('address/set-default/<int:address_id>/', views.set_default_address, name='set_default_address'),

    ]
