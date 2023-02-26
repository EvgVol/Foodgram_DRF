from django.conf import settings
from django.utils import timezone
from django.db import models
from django.shortcuts import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (permissions, response, status, views,
                            viewsets, generics, views)
from rest_framework.generics import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework.decorators import action
# from rest_framework.response import Response

from .serializers import (TagSerializer,
                          IngredientSerializer,
                          RecipeReadSerializer,
                          RecipeWriteSerializer,
                          ShowRecipeAddedSerializer
                        #   AddFavouriteRecipeSerializer,
                        #   ShoppingCartSerializer
                          )
from .filters import IngredientFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from recipes.models import (Ingredient, Tag, Recipe, Favorite
                            # IngredientInRecipe, , ShoppingCart
                            )
from users.permissions import IsAdminOrReadOnly, AuthorStaffOrReadOnly

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    filter_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для отображения рецептов.
    Для запросов на чтение используется RecipeReadSerializer
    Для запросов на изменение используется RecipeWriteSerializer"""

    queryset = Recipe.objects.all()
    permission_classes = (AuthorStaffOrReadOnly,)
    serializer_class = RecipeReadSerializer
    # filter_backends = [DjangoFilterBackend]
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
        """Добавляет/удалит рецепт в 'избранное'."""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        obj = Favorite.objects.filter(user=user, recipe__id=pk)

        if request.method == 'POST':
            if obj.exists():
                return response.Response(
                    {'warning': f'Нельзя второй раз добавить рецепт в избранное.'},
                    status=status.HTTP_400_BAD_REQUEST)
            serializer = ShowRecipeAddedSerializer(recipe)
            Favorite.objects.create(user=user, recipe=recipe)
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        if request.method == 'DELETE':
            if obj.exists():
                obj.delete()
                return response.Response(
                    {'message': f'Рецепт успешно удален из избранного'},
                    status=status.HTTP_204_NO_CONTENT)
            return response.Response(
                {'errors': 'Такого рецепта нет в избранном'},
                status=status.HTTP_400_BAD_REQUEST
            )








# class ShoppingCartView(views.APIView):
#     """Вьюсет для добавления рецепта в список покупок."""

#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, recipe_id):
#         user = request.user
#         data = {
#             'user': user.id,
#             'recipe': recipe_id,
#         }
#         context = {'request': request}
#         serializer = ShoppingCartSerializer(data=data, context=context)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return response.Response(
#             serializer.data, status=status.HTTP_201_CREATED
#         )

#     def delete(self, request, recipe_id):
#         user = request.user
#         recipe = generics.get_object_or_404(Recipe, id=recipe_id)
#         obj = ShoppingCart.objects.filter(user=user, recipe=recipe)
#         if obj.exists():
#             obj.delete()
#             return response.Response(status=status.HTTP_204_NO_CONTENT)
#         return response.Response(
#             {'errors': settings.WAS_DELETE},
#             status=status.HTTP_400_BAD_REQUEST)


# class DownloadShoppingCart(views.APIView):
#     """Вьюсет для выгрузки списка покупок в формате PDF."""

#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         shopping_list = {}
#         ingredients = IngredientInRecipe.objects.filter(
#             recipe__purchases__user=user
#         )
#         for ingredient in ingredients:
#             amount = ingredient.amount
#             name = ingredient.ingredient.name
#             measurement_unit = ingredient.ingredient.measurement_unit
#             if name not in shopping_list:
#                 shopping_list[name] = {
#                     'measurement_unit': measurement_unit,
#                     'amount': amount
#                 }
#             else:
#                 shopping_list[name]['amount'] += amount

#         pdfmetrics.registerFont(TTFont(
#             settings.FONT_NAME,
#             settings.FONT_NAME + '.ttf',
#             settings.ENCODING)
#         )

#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = ('attachment; '
#                                            'filename="shopping_list.pdf"')
#         page = canvas.Canvas(response)
#         page.setFont(settings.FONT_NAME, size=settings.SIZE_FRONT)
#         height = 750
#         width = 200
#         page.drawString(width, 800, 'Список ингредиентов')
#         for i, (item, value) in enumerate(shopping_list.items(), 1):
#             page.drawString(
#                 50,
#                 height,
#                 (f'<{i}> { item } - {value["amount"]}, '
#                  f'{value["measurement_unit"]}')
#             )
#             height -= 25
#         height -= 50
#         today_year = timezone.now().strftime("%Y")
#         page.drawString(width, height, f"Foodgram, {today_year}")
#         page.showPage()
#         page.save()
#         return
