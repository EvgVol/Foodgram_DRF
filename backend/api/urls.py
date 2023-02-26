from django.urls import include, path
from rest_framework import routers

from .views import (TagViewSet, IngredientViewSet, RecipeViewSet,
                    # FavoriteView, ShoppingCartView, DownloadShoppingCart
                    )


router = routers.DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
    # path(
    #     'recipes/<int:recipe_id>/favorite/',
    #     FavoriteView.as_view(),
    #     name='add_recipe_to_favorite'
    # ),
    # path(
    #     'recipes/<int:recipe_id>/shopping_cart/',
    #     ShoppingCartView.as_view(),
    #     name='add_recipe_to_shopping_cart'
    # ),
    # path(
    #     'recipes/download_shopping_cart/',
    #     DownloadShoppingCart.as_view(),
    #     name='download_shopping_cart'
    # ),
]
