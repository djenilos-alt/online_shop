from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Удаляет текущие данные и загружает каталог из фикстуры"

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(
            self.style.WARNING("Старые данные удалены.")
        )

        call_command("loaddata", "catalog_data.json")

        self.stdout.write(
            self.style.SUCCESS("Данные успешно загружены.")
        )
