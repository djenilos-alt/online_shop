from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product


User = get_user_model()


class ProductPermissionsTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@example.com",
            password="testpass123",
        )

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="testpass123",
        )

        self.moderator = User.objects.create_user(
            email="moderator@example.com",
            password="testpass123",
        )

        self.category = Category.objects.create(
            name="Тестовая категория",
            description="Категория для тестов",
        )

        content_type = ContentType.objects.get_for_model(Product)

        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=[
                "can_unpublish_product",
                "change_product",
                "delete_product",
            ],
        )

        self.moderator.user_permissions.add(*permissions)

        self.product = self.create_product()

    def create_product(self, **kwargs):
        data = {
            "name": "Тестовый продукт",
            "description": "Описание продукта",
            "category": self.category,
            "price": 100,
            "owner": self.owner,
            "is_published": True,
        }
        data.update(kwargs)

        return Product.objects.create(**data)

    def test_create_product_assigns_owner(self):
        """При создании продукта владельцем становится текущий пользователь."""
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("product_create"),
            {
                "name": "Новый продукт",
                "description": "Описание нового продукта",
                "category": self.category.pk,
                "price": "200.00",
            },
        )

        self.assertEqual(response.status_code, 302)

        product = Product.objects.get(name="Новый продукт")

        self.assertEqual(product.owner, self.owner)
        self.assertFalse(product.is_published)

    def test_owner_can_update_product(self):
        """Владелец может редактировать свой продукт."""
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("product_update", kwargs={"pk": self.product.pk}),
            {
                "name": "Изменённое название",
                "description": "Новое описание",
                "category": self.category.pk,
                "price": "150.00",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Изменённое название")

    def test_other_user_cannot_update_product(self):
        """Другой пользователь не может редактировать чужой продукт."""
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse("product_update", kwargs={"pk": self.product.pk}),
            {
                "name": "Чужое изменение",
                "description": "Описание",
                "category": self.category.pk,
                "price": "150.00",
            },
        )

        self.assertEqual(response.status_code, 403)

        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Тестовый продукт")

    def test_owner_can_delete_product(self):
        """Владелец может удалить свой продукт."""
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("product_delete", kwargs={"pk": self.product.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Product.objects.filter(pk=self.product.pk).exists()
        )

    def test_other_user_cannot_delete_product(self):
        """Другой пользователь не может удалить чужой продукт."""
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse("product_delete", kwargs={"pk": self.product.pk})
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Product.objects.filter(pk=self.product.pk).exists()
        )

    def test_moderator_can_update_any_product(self):
        """Модератор может редактировать чужой продукт."""
        self.client.force_login(self.moderator)

        response = self.client.post(
            reverse("product_update", kwargs={"pk": self.product.pk}),
            {
                "name": "Изменено модератором",
                "description": "Описание",
                "category": self.category.pk,
                "price": "300.00",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Изменено модератором")

    def test_moderator_can_delete_any_product(self):
        """Модератор может удалить чужой продукт."""
        self.client.force_login(self.moderator)

        response = self.client.post(
            reverse("product_delete", kwargs={"pk": self.product.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Product.objects.filter(pk=self.product.pk).exists()
        )

    def test_moderator_can_unpublish_product(self):
        """Модератор может отменить публикацию продукта."""
        self.client.force_login(self.moderator)

        response = self.client.post(
            reverse("product_unpublish", kwargs={"pk": self.product.pk})
        )

        self.assertEqual(response.status_code, 302)

        self.product.refresh_from_db()
        self.assertFalse(self.product.is_published)

    def test_other_user_cannot_unpublish_product(self):
        """Обычный пользователь не может отменить публикацию."""
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse("product_unpublish", kwargs={"pk": self.product.pk})
        )

        self.assertEqual(response.status_code, 403)

        self.product.refresh_from_db()
        self.assertTrue(self.product.is_published)
