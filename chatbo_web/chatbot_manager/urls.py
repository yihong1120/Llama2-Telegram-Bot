from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # 主頁面設為儀表板
    path('register/', views.register, name='register'),
    # path('login/', auth_views.LoginView.as_view(success_url='/chatbot_manager/'), name='login'),
    path('login/', views.home, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('view_log_file/<str:log_filename>/', views.view_log_file, name='view_log_file'),
    path('download_log_file/<str:log_filename>/', views.download_log_file, name='download_log_file'),
    path('view_json_file/<str:json_filename>/', views.view_json_file, name='view_json_file'),
    path('download_json_file/<str:json_filename>/', views.download_json_file, name='download_json_file'),
]
