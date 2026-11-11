from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Пользователь должен указать email")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("У администратора is_staff должен быть True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("У администратора is_superuser должен быть True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()

    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        verbose_name="Номер телефона",
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Страна",
    )

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
