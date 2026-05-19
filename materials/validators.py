from rest_framework.serializers import ValidationError


def validate_youtube_url(value):
    """Проверяет что ссылка ведёт только на youtube.com."""
    if value and 'youtube.com' not in value:
        raise ValidationError('Допускаются ссылки только на youtube.com')
    return value