from django.urls import path
from .views import submit_waste_request, my_requests, mark_as_completed, my_history

app_name = 'wasteapp'

urlpatterns = [
    path('submit/', submit_waste_request, name='submit_request'),
    path('my_requests/', my_requests, name='my_requests'),
    path('mark_as_completed/<int:request_id>/', mark_as_completed, name='mark_as_completed'),
    path('my_history/', my_history, name='my_history'),
]
