from celery import shared_task
from django.utils import timezone
from datetime import timedelta


@shared_task
def block_inactive_users():
    """
    Блокирует пользователей, которые не заходили более месяца.
    Обновление происходит батчем для оптимизации запросов к БД.
    """
    from .models import User

    month_ago = timezone.now() - timedelta(days=30)

    # Находим пользователей которые не заходили более месяца
    inactive_users = User.objects.filter(
        last_login__lt=month_ago,
        is_active=True
    )

    # Обновляем батчем — один запрос к БД вместо множества
    count = inactive_users.update(is_active=False)

    return f'Заблокировано пользователей: {count}'