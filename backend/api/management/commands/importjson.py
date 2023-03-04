from django.core.management import BaseCommand, CommandError
from django.db.utils import IntegrityError

from ._importjson import import_json


class Command(BaseCommand):
    """Импортер данных из json."""

    help = 'Импорт данных json из /data/ в базу данных.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Старт команды'))
        try:
            import_json()
        except IntegrityError:
            raise CommandError(
                'Очистите базу данных перед загрузкой файлов json,'
                ' воспользуйтесь менеджмент командой flush')
        except FileNotFoundError:
            raise CommandError(
                'Файлы json в папке data не найдены')
        except Exception:
            raise CommandError(
                'Непредвиденная ошибка при выполнении команды importjson,'
                ' обратитесь к разработчикам'
            )

        self.stdout.write(self.style.SUCCESS(
            'Все данные из json файлов загружены в базу данных'
        ))
