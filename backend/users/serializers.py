from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User
from .validators import validate_username, username_me


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для новых пользователей."""

    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            validate_username
        ]
    )

    class Meta:
        abstract = True
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', )

# class SingUpSerializer(serializers.Serializer):
#     """Сериализатор для регистрации."""

#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     username = serializers.CharField(
#         required=True,
#         validators=[validate_username, ]
#     )

#     def validate_username(self, value):
#         return username_me(value)


# class GetTokenSerializer(serializers.Serializer):
#     """Сериализатор для получения токена при регистрации."""

#     username = serializers.CharField(
#         required=True,
#         validators=(validate_username, )
#     )
#     confirmation_code = serializers.CharField(required=True)

#     def validate_username(self, value):
#         return username_me(value)



