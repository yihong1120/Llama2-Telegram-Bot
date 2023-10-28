from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('download_log/<int:log_id>/', views.download_log, name='download_log'),
]
