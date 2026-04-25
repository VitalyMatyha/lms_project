from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer
from .filters import PaymentFilter


class PaymentListView(generics.ListAPIView):
    """
    Список платежей с фильтрацией и сортировкой.
    Сортировка по дате оплаты: ?ordering=payment_date или ?ordering=-payment_date
    Фильтр по курсу: ?course=1
    Фильтр по уроку: ?lesson=1
    Фильтр по способу оплаты: ?payment_method=cash
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']  # сортировка по умолчанию — сначала новые


class UserUpdateView(generics.UpdateAPIView):
    """Обновление профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer