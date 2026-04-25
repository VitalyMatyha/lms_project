from django.urls import path
from .views import PaymentListView, UserUpdateView

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
]