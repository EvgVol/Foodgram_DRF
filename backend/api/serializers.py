from drf_extra_fields.fields import Base64ImageField
from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import serializers, relations, validators
from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.exceptions import ValidationError

from recipes.models import (Tag, Ingredient, Recipe, IngredientInRecipe, Favorite, ShoppingCart)
from users.serializers import UsersSerializer


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Tag."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор для вывода количество ингредиентов в рецепте."""

    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='ingredient'
    )

    name = serializers.SlugRelatedField(
        source='ingredient',
        read_only=True,
        slug_field='name'
    )

    measurement_unit = serializers.SlugRelatedField(
        source='ingredient',
        read_only=True,
        slug_field='measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = '__all__'


class RecipeReadSerializer(serializers.ModelSerializer):
    """ Сериализатор для возврата списка рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    author = UsersSerializer(read_only=True,
                             default=serializers.CurrentUserDefault())
    ingredients = SerializerMethodField()
    image = Base64ImageField()
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def get_ingredients(self, recipe):
        """Получает список ингредиентов для рецепта."""
        return IngredientInRecipeSerializer(recipe.recipe.all(), many=True).data

    def get_is_favorited(self, recipe):
        """Проверка - находится ли рецепт в избранном."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверка - находится ли рецепт в списке покупок."""
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return ShoppingCart.objects.filter(recipe=obj, user=user).exists()


class IngredientInRecipeWriteSerializer(serializers.ModelSerializer):
    """ Сериализатор для ингредиента в рецепте."""

    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all()
    )
    amount = IntegerField(write_only=True)

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeWriteSerializer(serializers.ModelSerializer):
    """ Сериализатор для создание рецептов."""

    tags = relations.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                            many=True)
    author = UsersSerializer(read_only=True)
    ingredients = IngredientInRecipeWriteSerializer(many=True)
    image = Base64ImageField(max_length=None, use_url=True)
    cooking_time = IntegerField()

    class Meta:
        model = Recipe
        fields = ('id', 'image', 'tags', 'author', 'ingredients',
                  'name', 'text', 'cooking_time')
        read_only_fields = ('author',)

    @transaction.atomic
    def create_bulk_ingredients(self, ingredients, recipe):
            IngredientInRecipe.objects.bulk_create(
                [IngredientInRecipe(
                    ingredient=ingredient['ingredient'],
                    recipe=recipe,
                    amount=ingredient['amount']
                ) for ingredient in ingredients]
            )

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients_list = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_bulk_ingredients(recipe, ingredients_list)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_bulk_ingredients(recipe=instance,
                                     ingredients=ingredients)
        instance.save()
        return instance

    def validate_ingredients(self, value):
        """Проверяем ингредиенты в рецепте."""
        ingredients = self.initial_data.get('ingredients')
        if len(ingredients) <= 0:
            raise ValidationError(
                {'ingredients': settings.INGREDIENT_MIN_AMOUNT_ERROR}
            )
        ingredients_list = []
        for item in ingredients:
            if item['id'] in ingredients_list:
                raise ValidationError(
                    {'ingredients': settings.INGREDIENT_DUBLICATE_ERROR}
                )
            ingredients_list.append(item['id'])
            if int(item['amount']) <= 0:
                raise ValidationError(
                    {'amount': settings.INGREDIENT_MIN_AMOUNT_ERROR}
                )
        return value

    def validate_cooking_time(self, data):
        """Проверяем время приготовления рецепта."""
        cooking_time = self.initial_data.get('cooking_time')
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                settings.COOKING_TIME_MIN_ERROR
            )
        return data

    def validate_tags(self, value):
        """Проверяем на наличие уникального тега."""
        tags = value
        if not tags:
            raise ValidationError(
                {'tags': settings.TAG_ERROR}
            )
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError(
                    {'tags': settings.TAG_UNIQUE_ERROR}
                )
            tags_list.append(tag)
        return value

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance,
                                    context=context).data


class ShowRecipeAddedSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe.
    Определён укороченный набор полей для некоторых эндпоинтов."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    # def get_image(self, obj):
    #     """Получаем изображение рецепта."""
    #     request = self.context.get('request')
    #     photo_url = obj.image.url
    #     return request.build_absolute_uri(photo_url)


class AddFavouriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор добавления рецепта в избранное."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message=settings.RECIPE_IN_FAVORITE
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return ShowRecipeAddedSerializer(
            instance.recipe,
            context={'request': request}
        ).data


# class ShoppingCartSerializer(AddFavouriteRecipeSerializer):
#     """Сериализатор совершения покупок"""

#     class Meta(AddFavouriteRecipeSerializer.Meta):
#         model = ShoppingCart
#         validators = [
#             validators.UniqueTogetherValidator(
#                 queryset=ShoppingCart.objects.all(),
#                 fields=['user', 'recipe'],
#                 message=settings.ALREADY_BUY
#             )
#         ]

#     def to_representation(self, instance):
#         request = self.context.get('request')
#         return ShowRecipeAddedSerializer(
#             instance.recipe,
#             context={'request': request}
#         ).data
