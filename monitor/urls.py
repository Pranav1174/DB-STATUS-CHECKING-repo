from django.urls import path
from .views import get_db_status

urlpatterns = [
    path('status/', get_db_status),
]
