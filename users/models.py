from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    company_name = models.TextField(
        verbose_name="Название компании", help_text="Введите название компании", **NULLABLE
    )
    inn = models.CharField(max_length=12, verbose_name='ИНН', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
