from datetime import datetime as dt

from django.db.models import Sum
from django.shortcuts import HttpResponse
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (TagSerializer,
                          IngredientSerializer,
                          RecipeReadSerializer,
                          RecipeWriteSerializer)
from .filters import IngredientFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import AdminOrAuthorOrReadOnly
from recipes.models import (Ingredient, Tag, Recipe, Favorite,
                            ShoppingCart, IngredientInRecipe)
from core.option import add_and_del


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
    filter_class = RecipeFilter
    pagination_class = LimitPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
            if self.request.method in ('POST', 'PUT', 'PATCH'):
                return RecipeWriteSerializer
            return RecipeReadSerializer

    @action(
            detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=[permissions.IsAuthenticated]
        )
    def favorite(self, request, pk):
        return add_and_del(self, Favorite, request, pk)

    @action(
            detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=[permissions.IsAuthenticated]
        )
    def shopping_cart(self, request, pk):
        """Добавляем/удаляем рецепт в 'список покупок'"""
        return add_and_del(self, ShoppingCart, request, pk)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """Загружает файл *.txt со списком покупок.
        Доступно только авторизованным пользователям.
        """
        user = self.request.user
        if not user.shopping_list.exists():
            return Response(
                {"error": "Вы не сделали покупку"},
                status=status.HTTP_400_BAD_REQUEST
            )
        filename = f'{user.username}_shopping_list.txt'

        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_list__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        today = dt.today()
        shopping_list = (
            f'Список покупок для пользователя: {user.username}\n\n'
            f'Дата: {today:%Y-%m-%d}\n\n'
        )
        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])
        shopping_list += f'\n\nFoodgram ({today:%Y})'

        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
