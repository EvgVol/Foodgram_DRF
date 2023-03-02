import csv
import os

from django.conf import settings

from recipes.models import Ingredient, Tag


FILE_DIR = os.path.join(
    settings.BASE_DIR,
    'data'
)

def import_csv():
    """Импортер данных из csv."""
    with open(
        os.path.join(FILE_DIR, "ingredients.csv"), encoding="utf-8"
    ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        Ingredient.objects.bulk_create(objs=[
            Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit'],
            )
            for row in reader
        ])
        print(f'Файл {csvfile.name} загружен.')

    with open(
        os.path.join(FILE_DIR, "tags.csv"), encoding="utf-8"
    ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        Tag.objects.bulk_create(objs=[
            Tag(
                name=row['name'],
                color=row['color'],
                slug=row['slug'],
            )
            for row in reader
        ])
        print(f'Файл {csvfile.name} загружен.')
