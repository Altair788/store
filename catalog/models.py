from django.db import models


class Category(models.Model):
    """
    Представляет класс Категория
    """
    title = models.CharField(max_length=200, verbose_name='Категория')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    """
    Представляет класс Продукт
    """
    title = models.CharField(max_length=200, verbose_name='Продукт')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'