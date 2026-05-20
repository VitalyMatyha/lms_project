from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Payment
from .serializers import UserSerializer, UserRegisterSerializer, PaymentSerializer
from .filters import PaymentFilter
from rest_framework.response import Response
from .services import create_stripe_product, create_stripe_price, create_stripe_session
from .serializers import PaymentCreateSerializer


class PaymentCreateView(generics.CreateAPIView):
    """
    Создание платежа с интеграцией Stripe.
    Возвращает ссылку на оплату.
    """

    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Создаём платёж и получаем ссылку на оплату через Stripe."""
        payment = serializer.save(user=self.request.user)

        # Получаем название продукта
        product_name = payment.course.title if payment.course else payment.lesson.title

        # Создаём продукт, цену и сессию в Stripe
        stripe_product_id = create_stripe_product(product_name)
        stripe_price_id = create_stripe_price(stripe_product_id, int(payment.amount))
        session_id, payment_url = create_stripe_session(stripe_price_id)

        # Сохраняем данные Stripe в модель
        payment.stripe_product_id = stripe_product_id
        payment.stripe_price_id = stripe_price_id
        payment.stripe_session_id = session_id
        payment.payment_url = payment_url
        payment.save()

    def create(self, request, *args, **kwargs):
        """Возвращаем ссылку на оплату в ответе."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        payment = serializer.instance
        return Response({
            'payment_id': payment.pk,
            'payment_url': payment.payment_url,
            'status': payment.status,
        }, status=status.HTTP_201_CREATED)

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


