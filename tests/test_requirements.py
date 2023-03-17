import os

from django.conf import settings


class Test01Requirements:

    def test_requirements(self):
        try:
            with open(
                f'{os.path.join(settings.BASE_DIR, "requirements.txt")}', 'r'
            ) as f:
                requirements = f.read()
        except FileNotFoundError:
            assert False, 'Проверьте, что добавили файл requirements.txt'

        assert 'gunicorn' in requirements, (
            'Проверьте, что добавили gunicorn в файл requirements.txt'
        )
        assert 'django' in requirements, (
            'Проверьте, что добавили django в файл requirements.txt'
        )
        assert 'djoser' in requirements, (
            'Проверьте, что добавили djoser в файл requirements.txt'
        )
        assert 'djangorestframework' in requirements, (
            'Проверьте, что добавили djangorestframework в файл '
            'requirements.txt'
        )
        assert 'drf-extra-fields' in requirements, (
            'Проверьте, что добавили drf-extra-fields в файл requirements.txt'
        )
