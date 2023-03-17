import pytest
import json

from recipes.models import Ingredient, Tag, Recipe


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


@pytest.fixture
def new_recipe():
    recipe = {
        "ingredients": [json.dumps({"id": 1, "amount": 10}), ],
        "tags": [1, 2],
        "image": ('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA'
                  'EAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAA'
                  'AACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAgg'
                  'CByxOyYQAAAABJRU5ErkJggg=='),
        "name": "string",
        "text": "string",
        "cooking_time": 1
    }
    return recipe


@pytest.fixture
def recipes():
    return ('/api/recipes/')
