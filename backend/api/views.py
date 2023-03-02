from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, viewsets, decorators, response, status

from .filters import IngredientFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import AdminOrAuthorOrReadOnly
from .serializers import (FollowSerializer, UsersSerializer,
                          IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, TagSerializer,
                          AddFavoriteRecipeSerializer,
                          AddShoppingListRecipeSerializer,)
from .utils import add_and_del, out_list_ingredients
from recipes.models import (Favorite, Ingredient,
                            Recipe, ShoppingCart, Tag)
from users.models import Follow, User


class CustomUserViewSet(UserViewSet):
    """Вьюсет для кастомной модели пользователя."""

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = LimitPageNumberPagination

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        """Подписываем / отписываемся на пользователя.
        Доступно только авторизованным пользователям.
        """
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer = FollowSerializer(author,
                                          data=request.data,
                                          context={'request': request})
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return response.Response(status=status.HTTP_201_CREATED)
        else:
            subscription = get_object_or_404(Follow,
                                             user=user,
                                             author=author)
            subscription.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)

    @decorators.action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscriptions(self, request):
        """Возвращает пользователей, на которых подписан текущий пользователь.
        В выдачу добавляются рецепты.
        """
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(pages,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    filter_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для отображения рецептов.
    Для запросов на чтение используется RecipeReadSerializer
    Для запросов на изменение используется RecipeWriteSerializer"""

    queryset = Recipe.objects.all()
    permission_classes = (AdminOrAuthorOrReadOnly,)
    serializer_class = RecipeReadSerializer
    filterset_class = RecipeFilter
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
            if self.request.method in ('POST', 'PUT', 'PATCH'):
                return RecipeWriteSerializer
            return RecipeReadSerializer

    @decorators.action(
            detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=[permissions.IsAuthenticated]
        )
    def favorite(self, request, pk):
        return add_and_del(
            self, AddFavoriteRecipeSerializer, Favorite, request, pk
        )

    @decorators.action(
            detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=[permissions.IsAuthenticated]
        )
    def shopping_cart(self, request, pk):
        """Добавляем/удаляем рецепт в 'список покупок'"""
        return add_and_del(
            self, AddShoppingListRecipeSerializer, ShoppingCart, request, pk
        )

    @decorators.action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        return out_list_ingredients(self, request)
