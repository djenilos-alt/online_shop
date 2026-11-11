from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail

from users.models import User


class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            email="user@example.com",
            password="TestPassword123",
        )

        self.assertEqual(user.email, "user@example.com")
        self.assertTrue(user.check_password("TestPassword123"))
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            password="AdminPassword123",
        )

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
)
class UserRegistrationTest(TestCase):

    def test_registration(self):
        response = self.client.post(
            reverse("users:register"),
            {
                "email": "newuser@example.com",
                "password1": "TestPassword123",
                "password2": "TestPassword123",
            },
        )

        self.assertRedirects(
            response,
            reverse("users:login"),
        )

        self.assertTrue(
            User.objects.filter(email="newuser@example.com").exists()
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].to,
            ["newuser@example.com"],
        )
