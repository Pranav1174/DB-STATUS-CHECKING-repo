from django.urls import path
from .views import get_db_status

urlpatterns = [
    path('db-status/', get_db_status, name='db_status'),
]
