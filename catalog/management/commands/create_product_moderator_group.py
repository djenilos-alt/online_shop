from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from catalog.models import Product


class Command(BaseCommand):
    help = "Создаёт группу модераторов продуктов и назначает ей права"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(
            name="Модератор продуктов"
        )

        content_type = ContentType.objects.get_for_model(Product)

        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=[
                "can_unpublish_product",
                "delete_product",
                "change_product",
            ],
        )

        group.permissions.set(permissions)

        self.stdout.write(
            self.style.SUCCESS(
                f"Группа «{group.name}» успешно настроена."
            )
        )

        if permissions.count() != 3:
            self.stdout.write(
                self.style.WARNING(
                    "Проверьте наличие всех трёх разрешений."
                )
            )
