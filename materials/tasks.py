from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_course_update_email(course_id):
    """
    Отправляет письма подписчикам курса об обновлении материалов.
    Письмо отправляется только если курс не обновлялся более 4 часов.
    """
    from .models import Course, Subscription

    course = Course.objects.get(pk=course_id)

    # Дополнительное задание: проверяем что курс не обновлялся более 4 часов
    time_since_update = timezone.now() - course.updated_at
    if time_since_update < timedelta(hours=4):
        return 'Курс обновлялся менее 4 часов назад — письма не отправляются'

    # Получаем всех подписчиков курса
    subscriptions = Subscription.objects.filter(course=course).select_related('user')

    for subscription in subscriptions:
        send_mail(
            subject=f'Обновление курса: {course.title}',
            message=f'Курс "{course.title}" был обновлён. Заходите и смотрите новые материалы!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=False,
        )

    return f'Отправлено писем: {subscriptions.count()}'