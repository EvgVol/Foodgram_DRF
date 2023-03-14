import pytest

from recipes.models import Tag, Ingredient


@pytest.fixture
def tag_breakfast():
    return Tag.objects.create(
        name='Завтрак', color='#E26C2D', slug='breakfast'
    )


@pytest.fixture
def tag_dinner():
    return Tag.objects.create(
        name='Обед', color='#ffff00', slug='dinner'
    )


@pytest.fixture
def tag_supper():
    return Tag.objects.create(
        name='Ужин', color='#ff0000', slug='supper'
    )


@pytest.fixture
def ingredient_1():
    return Ingredient.objects.create(
        name='Масло', measurement_unit='г'
    )


@pytest.fixture
def ingredient_2():
    return Ingredient.objects.create(
        name='Яйцо', measurement_unit='шт'
    )


@pytest.fixture
def ingredient_3():
    return Ingredient.objects.create(
        name='Колбаса', measurement_unit='г'
    )
