from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModer, IsOwner


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