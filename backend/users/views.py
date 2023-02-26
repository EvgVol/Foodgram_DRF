from djoser.views import UserViewSet
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from .serializers import FollowSerializer, UserPasswordSerializer, UsersSerializer
from api.pagination import LimitPageNumberPagination


class CustomUserViewSet(UserViewSet):
    """Вьюсет для кастомной модели пользователя."""

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = LimitPageNumberPagination

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer = FollowSerializer(author,
                                          data=request.data,
                                          context={'request': request})
            if user == author:
                return Response(
                    {'errors': 'Вы не можете подписываться на самого себя.'},
                    status=status.HTTP_400_BAD_REQUEST)
            if Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'warning': f'Нельзя второй раз подписаться на пользователя {author.username}.'},
                    status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                Follow.objects.create(user=user, author=author)
                return Response(
                    {'message': f'Вы подписаны на пользователя {author.username}'},
                    status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = get_object_or_404(Follow, user=user, author=author)
            subscription.delete()
            return Response(
                {'message': f'Вы успешно отписались от пользователя {author.username}'},
                status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        """Получить на кого пользователь подписан."""
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(pages,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)


@api_view(['post'])
def set_password(request):
    """Изменяем пароль."""
    serializer = UserPasswordSerializer(
        data=request.data,
        context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': settings.PASSWORD_CHANGED},
            status=status.HTTP_201_CREATED)
    return Response(
        {'error': settings.PASSWORD_INCORRECT},
        status=status.HTTP_400_BAD_REQUEST)