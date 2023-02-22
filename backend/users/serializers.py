from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, validators

from .models import User, Follow
from .validators import validate_username
from recipes.models import Recipe
from api.serializers import ShowRecipeAddedSerializer


class UserRegistrationSerializer(UserCreateSerializer):
    """Сериализатор для новых пользователей."""

    username = serializers.CharField(
        required=True,
        validators=[
            validators.UniqueValidator(queryset=User.objects.all()),
            validate_username
        ]
    )

    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'email', 'first_name', 'last_name',)
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class UsersSerializer(UserSerializer):
    """Сериализатор для всех пользователей."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username','password',
                  'first_name', 'last_name', 'is_subscribed',)
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = 'is_subscribed',

    def get_is_subscribed(self, obj):
        """Проверка подписки пользователей."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()

class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор вывода авторов на которых подписан текущий пользователь."""

    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                    'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = '__all__',

    def get_is_subscribed(self, obj):
        """Проверка подписки пользователей."""
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return ShowRecipeAddedSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        """ Показывает общее количество рецептов у каждого автора."""
        return Recipe.objects.filter(author=obj.author).count()
