from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegisterView, UserListView, UserDetailView,
    UserUpdateView, UserDeleteView, PaymentListView
)

urlpatterns = [
    # Авторизация — открытые эндпоинты
    path('users/register/', UserRegisterView.as_view(), name='user-register'),
    path('users/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # CRUD пользователей
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),

    # Платежи
    path('payments/', PaymentListView.as_view(), name='payment-list'),
]