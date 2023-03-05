from colorfield.fields import ColorField
from django.conf import settings
from django.core import validators
from django.db import models

from users.models import User


class FavoriteAndShoppingCartModel(models.Model):
    """Абстрактная модель. Добавляет юзера и рецепт."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Пользователь',
    )

    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class IngredientTagRecipe(models.Model):
    """Абстрактная модель. Добавляет название."""

    name = models.CharField(
        'Название',
        unique=True,
        max_length=settings.LENG_MAX,
        help_text=settings.MAX_NUMBER_OF_CHARACTERS
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Ingredient(IngredientTagRecipe):
    """Модель списка ингредиентов."""

    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=settings.LENG_MAX,
        help_text=settings.MAX_NUMBER_OF_CHARACTERS
    )

    class Meta(IngredientTagRecipe.Meta):
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique_ingredient')
        ]


class Tag(IngredientTagRecipe):
    """Модель тегов."""

    color = ColorField(
        'Цветовой HEX-код',
        unique=True,
        default='#FF0000',
        max_length=settings.LENG_COLOR,
        validators=[
            validators.RegexValidator(
                regex=settings.COLOR_REGEX,
                message=settings.NOT_COLOR_HEX
            ),
        ],
        error_messages={'unique': settings.COLOR_NO_UNIQUE},
        help_text=settings.HELP_CHOISE_COLOR
    )

    slug = models.SlugField(
        'Уникальный слаг',
        unique=True,
        max_length=settings.LENG_MAX,
        help_text=settings.SLUG_NOTIFICATION,
        validators=[validators.validate_slug],
    )

    class Meta(IngredientTagRecipe.Meta):
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        default_related_name = 'tags'
        ordering = ('name',)


class Recipe(IngredientTagRecipe):
    """Модель рецептов."""

    author = models.ForeignKey(User, verbose_name='Автор рецепта',
                               on_delete=models.SET_NULL, null=True,)

    text = models.TextField('Описание рецепта')

    image = models.ImageField('Изображение блюда', upload_to='recipes/')

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
        through='IngredientInRecipe',
        verbose_name='Ингредиенты',
    )

    tags = models.ManyToManyField(Tag, verbose_name='Теги')

    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False,
    )

    class Meta(IngredientTagRecipe.Meta):
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipes'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_for_author',
            ),
        )


class IngredientInRecipe(models.Model):
    """Количество ингредиентов в рецепте.
    Модель связывает Recipe и Ingredient с указанием количества ингредиентов.
    """

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredient_list'
    )

    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredient_list',
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
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe'
            )
        ]

    def __str__(self):
        return (
            f'{self.ingredient.name} ({self.ingredient.measurement_unit})'
            f' - {self.amount}'
        )


class Favorite(FavoriteAndShoppingCartModel):
    """Модель избранного."""

    class Meta(FavoriteAndShoppingCartModel.Meta):
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        default_related_name = 'favorites'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_user_recipe',
            ),
        )


class ShoppingCart(FavoriteAndShoppingCartModel):
    """Рецепты в корзине покупок.
    Модель связывает Recipe и  User.
    """

    class Meta(FavoriteAndShoppingCartModel.Meta):
        verbose_name = 'покупка'
        verbose_name_plural = 'покупки'
        default_related_name = 'shopping_list'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_shopping')
        ]
