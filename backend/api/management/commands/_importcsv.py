import csv
import os

from django.conf import settings

from recipes.models import Ingredient, Tag


FILE_DIR = os.path.join(settings.BASE_DIR, 'data')


def import_csv():
    """Импортер данных из csv."""
    with open(
        os.path.join(FILE_DIR, 'ingredients.csv'), 'r', encoding='utf-8'
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name, measurement_unit = row
            Ingredient.objects.get_or_create(
                name=name, measurement_unit=measurement_unit
            )
        print(f'Файл {csvfile.name} загружен.')

    with open(
        os.path.join(FILE_DIR, 'tags.csv'), 'r', encoding='utf-8'
    ) as csvfile:
        reader_tags = csv.reader(csvfile)
        for row in reader_tags:
            name, color, slug = row
            Tag.objects.get_or_create(name=name,
                                      color=color,
                                      slug=slug)
        print(f'Файл {csvfile.name} загружен.')
