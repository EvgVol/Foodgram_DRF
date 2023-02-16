from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, permissions, response,
                            status, views, viewsets)
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import (GetTokenSerializer, SingUpSerializer,
                          UsersSerializer)


class SignUp(views.APIView):
    """Функция регистрации новых пользователей."""

    serializer_class = SingUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(
                username=serializer.validated_data.get('username'),
                email=serializer.validated_data.get('email')
            )
        except IntegrityError:
            return response.Response(
                settings.MESSAGE_EMAIL_EXISTS if
                User.objects.filter(username='username').exists()
                else settings.MESSAGE_USERNAME_EXISTS,
                status.HTTP_400_BAD_REQUEST
            )
        code = default_token_generator.make_token(user)
        send_mail(
            'Код токена',
            f'Код для получения токена {code}',
            settings.DEFAULT_FROM_EMAIL,
            [serializer.validated_data.get('email')]
        )
        return response.Response(
            serializer.data, status=status.HTTP_200_OK
        )


@api_view(['POST'])
def get_token(request):
    """Функция получения токена при регистрации."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data.get(
        'confirmation_code'
    )
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return response.Response(
            {'token': str(token)}, status=status.HTTP_200_OK
        )
    return response.Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
    search_fields = ('username', )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = PersSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(
                serializer.data, status=status.HTTP_200_OK
            )
        serializer = PersSerializer(user)
        return response.Response(
            serializer.data, status=status.HTTP_200_OK
        )