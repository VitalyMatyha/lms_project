from rest_framework import serializers
from .models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели платежа."""

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра и редактирования профиля пользователя."""

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'payments']


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'phone', 'city', 'avatar']

    def validate_email(self, value):
        """Проверяем что пользователь с таким email не существует."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует.')
        return value

    def create(self, validated_data):
        """Создаём пользователя с хешированным паролем."""
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone'),
            city=validated_data.get('city'),
            avatar=validated_data.get('avatar'),
        )
        return user


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания платежа с интеграцией Stripe."""

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'amount', 'payment_method']