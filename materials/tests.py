from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Course, Lesson, Subscription
from users.models import User


class LessonCRUDTestCase(APITestCase):
    """Тесты CRUD для уроков."""

    def setUp(self):
        """Создаём тестовые данные."""
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Описание урока',
            course=self.course,
            owner=self.user,
            video_url='https://youtube.com/watch?v=test'
        )

    def test_lesson_list(self):
        """Тест получения списка уроков."""
        url = reverse('lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_create(self):
        """Тест создания урока."""
        url = reverse('lesson-create')
        data = {
            'title': 'Новый урок',
            'description': 'Описание',
            'course': self.course.pk,
            'video_url': 'https://youtube.com/watch?v=new'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_create_invalid_url(self):
        """Тест создания урока с невалидной ссылкой."""
        url = reverse('lesson-create')
        data = {
            'title': 'Новый урок',
            'description': 'Описание',
            'course': self.course.pk,
            'video_url': 'https://vimeo.com/watch?v=new'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_retrieve(self):
        """Тест получения одного урока."""
        url = reverse('lesson-detail', args=[self.lesson.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update(self):
        """Тест обновления урока."""
        url = reverse('lesson-update', args=[self.lesson.pk])
        data = {'title': 'Обновлённый урок', 'course': self.course.pk}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_delete(self):
        """Тест удаления урока."""
        url = reverse('lesson-delete', args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_create_unauthenticated(self):
        """Тест создания урока без авторизации."""
        self.client.force_authenticate(user=None)
        url = reverse('lesson-create')
        data = {'title': 'Урок', 'course': self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubscriptionTestCase(APITestCase):
    """Тесты для подписки на курс."""

    def setUp(self):
        """Создаём тестовые данные."""
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание',
            owner=self.user
        )

    def test_subscription_create(self):
        """Тест создания подписки."""
        url = reverse('subscription')
        response = self.client.post(url, {'course_id': self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')

    def test_subscription_delete(self):
        """Тест удаления подписки."""
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse('subscription')
        response = self.client.post(url, {'course_id': self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')

    def test_subscription_unauthenticated(self):
        """Тест подписки без авторизации."""
        self.client.force_authenticate(user=None)
        url = reverse('subscription')
        response = self.client.post(url, {'course_id': self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)