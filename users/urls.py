from django.urls import path
from .views import UserUpdateView

urlpatterns = [
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
]