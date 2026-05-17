from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Payment
from .serializers import UserSerializer, UserRegisterSerializer, PaymentSerializer
from .filters import PaymentFilter


class UserRegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя. Доступна без авторизации."""

    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserListView(generics.ListAPIView):
    """Список всех пользователей. Только для авторизованных."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveAPIView):
    """Просмотр профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserUpdateView(generics.UpdateAPIView):
    """Обновление профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDeleteView(generics.DestroyAPIView):
    """Удаление пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class PaymentListView(generics.ListAPIView):
    """
    Список платежей с фильтрацией и сортировкой.
    Сортировка: ?ordering=payment_date или ?ordering=-payment_date
    Фильтры: ?course=1, ?lesson=1, ?payment_method=cash
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']