from django.conf import settings
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User


class Ingredient(models.Model):
    """Модель списка ингредиентов."""

    name = models.CharField(
        'Название ингредиента',
        max_length=settings.LENG_MAX,
        help_text=f'Набор символов не более {settings.LENG_MAX}.'
    )

    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=settings.LENG_MAX,
        help_text=f'Набор символов не более {settings.LENG_MAX}.'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient')
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        'Название',
        unique=True,
        max_length=settings.LENG_MAX,
        help_text=f'Набор символов не более {settings.LENG_MAX}.'
    )

    color = models.CharField(
        'Цветовой HEX-код',
        unique=True,
        default='#ffffff',
        max_length=settings.LENG_COLOR,
        validators=[
            validators.RegexValidator(
                regex=settings.COLOR_REGEX,
                message=settings.NOT_COLOR_HEX
            ),
        ],
        error_messages={
            'unique': "Такой цвет уже существует!",
        },
        help_text=f'Набор символов не более {settings.LENG_COLOR}.'
    )

    slug =  models.SlugField(
        'Уникальный слаг',
        unique=True,
        max_length=settings.LENG_MAX,
        help_text=settings.SLUG_NOTIFICATION,
        validators=[validators.validate_slug],
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    name = models.CharField(
        'Название',
        max_length=settings.LENG_MAX
    )

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
    )

    text = models.TextField(
        'Описание рецепта'
    )

    image = models.ImageField(
        'Изображение блюда',
        upload_to='recipes/'
    )

    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        default=settings.COOKING_TIME_MIN_VALUE,
        validators=[
            validators.MinValueValidator(
                settings.COOKING_TIME_MIN_VALUE,
                message=settings.COOKING_TIME_MIN_ERROR
            ),
        ],
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_for_author',
            ),
        )

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """Количество ингредиентов в рецепте.
    Модель связывает Recipe и Ingredient с указанием количества ингредиентов.
    """

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    ingredients = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиенты',
        on_delete=models.CASCADE,
        related_name='recipe',
    )

    amount = models.PositiveSmallIntegerField(
        default=settings.INGREDIENT_MIN_AMOUNT,
        validators=(
            validators.MinValueValidator(
                settings.INGREDIENT_MIN_AMOUNT,
                message=settings.INGREDIENT_MIN_AMOUNT_ERROR
            ),
        ),
        verbose_name='Количество',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredients_recipe'
            )
        ]

    def __str__(self):
        return (
            f'{self.ingredient.name} - {self.amount}'
            f' ({self.ingredient.measurement_unit})'
        )


class Favorite(models.Model):
    """Модель избранного."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='favorites',
        verbose_name='Пользователь',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_user_recipe',
            ),
        )

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Избранное'


class ShoppingCart(models.Model):
    """Рецепты в корзине покупок.
    Модель связывает Recipe и  User.
    """

    user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        null=True,
    ),

    recipe = models.ManyToManyField(
        Recipe,
        verbose_name='Рецепт',
        related_name='shopping_cart',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user', ),
                name='unique_cart_user',
            ),
        )

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'
