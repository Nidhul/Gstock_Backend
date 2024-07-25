# register/urls.py

from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, get_non_admin_users, delete_user

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
     path('non-admin-users/', get_non_admin_users, name='get_non_admin_users'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
]
