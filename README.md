# LMS Project

Платформа для онлайн-обучения на Django REST Framework.

## Стек технологий

- Django 6 + DRF
- PostgreSQL
- Redis + Celery
- Docker + Docker Compose

## Запуск проекта

### 1. Клонируй репозиторий
git clone <ссылка на репозиторий>
cd lms_project

### 2. Создай .env файл
Скопируй .env.example в .env и заполни значения:
cp .env.example .env

### 3. Запусти проект
docker-compose up --build

### 4. Создай суперпользователя (в отдельном терминале)
docker-compose exec app python manage.py createsuperuser

## Доступные эндпоинты

- API: http://localhost:8000/
- Документация: http://localhost:8000/api/docs/
- Админка: http://localhost:8000/admin/

## Остановка проекта
docker-compose down

## Остановка с удалением данных
docker-compose down -v