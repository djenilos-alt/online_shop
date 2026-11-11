from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from blog.models import BlogPost


User = get_user_model()


class BlogPermissionsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpass123",
        )

        self.moderator = User.objects.create_user(
            email="moderator@example.com",
            password="testpass123",
        )

        self.content_manager = User.objects.create_user(
            email="manager@example.com",
            password="testpass123",
        )

        # Создаём группу модераторов продуктов.
        moderator_group, _ = Group.objects.get_or_create(
            name="Модератор продуктов"
        )

        # Назначаем модератору только права на продукты.
        product_permissions = Permission.objects.filter(
            content_type__app_label="catalog",
            codename__in=[
                "can_unpublish_product",
                "change_product",
                "delete_product",
            ],
        )
        moderator_group.permissions.set(product_permissions)
        self.moderator.groups.add(moderator_group)

        # Назначаем контент-менеджеру права на блог.
        content_manager_group, _ = Group.objects.get_or_create(
            name="Контент-менеджер"
        )

        blog_permissions = Permission.objects.filter(
            content_type__app_label="blog",
            codename__in=[
                "add_blogpost",
                "change_blogpost",
                "delete_blogpost",
                "view_blogpost",
            ],
        )
        content_manager_group.permissions.set(blog_permissions)
        self.content_manager.groups.add(content_manager_group)

        self.post = BlogPost.objects.create(
            title="Тестовая запись",
            content="Содержимое тестовой записи",
            is_published=True,
        )

    def test_anonymous_user_sees_only_published_posts(self):
        BlogPost.objects.create(
            title="Черновик",
            content="Неопубликованная запись",
            is_published=False,
        )

        response = self.client.get(reverse("blog:post_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 1)

    def test_regular_user_cannot_create_post(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("blog:post_create"))

        self.assertEqual(response.status_code, 403)

    def test_product_moderator_cannot_manage_blog(self):
        self.client.force_login(self.moderator)

        urls = [
            reverse("blog:post_create"),
            reverse("blog:post_update", kwargs={"pk": self.post.pk}),
            reverse("blog:post_delete", kwargs={"pk": self.post.pk}),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

    def test_content_manager_can_create_post(self):
        self.client.force_login(self.content_manager)

        response = self.client.get(reverse("blog:post_create"))

        self.assertEqual(response.status_code, 200)

    def test_content_manager_can_update_post(self):
        self.client.force_login(self.content_manager)

        response = self.client.get(
            reverse("blog:post_update", kwargs={"pk": self.post.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_content_manager_can_delete_post(self):
        self.client.force_login(self.content_manager)

        response = self.client.get(
            reverse("blog:post_delete", kwargs={"pk": self.post.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_content_manager_can_see_unpublished_posts(self):
        unpublished_post = BlogPost.objects.create(
            title="Черновик",
            content="Неопубликованная запись",
            is_published=False,
        )

        self.client.force_login(self.content_manager)

        response = self.client.get(reverse("blog:post_list"))

        self.assertContains(response, unpublished_post.title)
