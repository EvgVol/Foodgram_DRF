import json
import os

from django.conf import settings

from recipes.models import Ingredient, Tag


FILE_DIR = os.path.join(settings.BASE_DIR, 'data')


def import_json():
    """Импортер данных из json."""
    with open(
        os.path.join(FILE_DIR, 'ingredients.json'), encoding='utf-8'
    ) as data_file_ingredients:
        ingredient_data = json.loads(data_file_ingredients.read())
        for ingredients in ingredient_data:
            Ingredient.objects.get_or_create(**ingredients)
        print(f'Файл {data_file_ingredients.name} загружен.')

    with open(
        os.path.join(FILE_DIR, 'tags.json'), encoding='utf-8'
    ) as data_file_tags:
        tag_data = json.loads(data_file_tags.read())
        for tags in tag_data:
            Tag.objects.get_or_create(**tags)
        print(f'Файл {data_file_tags.name} загружен.')
