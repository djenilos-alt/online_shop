from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from blog.models import BlogPost


class Command(BaseCommand):
    help = "Создаёт группу контент-менеджеров и назначает ей права"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(
            name="Контент-менеджер"
        )

        content_type = ContentType.objects.get_for_model(BlogPost)

        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=[
                "add_blogpost",
                "change_blogpost",
                "delete_blogpost",
                "view_blogpost",
            ],
        )

        group.permissions.set(permissions)

        self.stdout.write(
            self.style.SUCCESS(
                f"Группа «{group.name}» успешно настроена."
            )
        )

        if permissions.count() != 4:
            self.stdout.write(
                self.style.WARNING(
                    "Проверьте наличие всех четырёх разрешений."
                )
            )
