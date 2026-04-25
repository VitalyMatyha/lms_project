import django_filters
from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    """Фильтр для модели платежа."""

    class Meta:
        model = Payment
        fields = {
            'course': ['exact'],       # фильтр по курсу
            'lesson': ['exact'],       # фильтр по уроку
            'payment_method': ['exact'],  # фильтр по способу оплаты
        }