from rest_framework import viewsets, generics
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModer, IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Subscription
from .paginators import MaterialsPagination

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели курса.
    Модераторы могут просматривать и редактировать, но не создавать и удалять.
    Обычные пользователи работают только со своими курсами.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == 'create':
            # Создавать могут только не-модераторы
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action == 'destroy':
            # Удалять могут только владельцы
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            # Редактировать могут модераторы или владельцы
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        else:
            # Список — все авторизованные
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """Привязываем курс к авторизованному пользователю."""
        serializer.save(owner=self.request.user)


class LessonListView(generics.ListAPIView):
    """Список уроков. Доступен всем авторизованным."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonCreateView(generics.CreateAPIView):
    """Создание урока. Модераторы не могут создавать."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        """Привязываем урок к авторизованному пользователю."""
        serializer.save(owner=self.request.user)


class LessonDetailView(generics.RetrieveAPIView):
    """Просмотр урока. Модераторы или владельцы."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateView(generics.UpdateAPIView):
    """Редактирование урока. Модераторы или владельцы."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDeleteView(generics.DestroyAPIView):
    """Удаление урока. Только владельцы."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionView(APIView):
    """
    Управление подпиской на курс.
    POST — подписывает или отписывает пользователя от курса.
    """

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для модели курса."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPagination
    # ... остальной код


class LessonListView(generics.ListAPIView):
    """Список уроков."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialsPagination