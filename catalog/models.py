from django.db import models

NULLABLE = {"blank": True, "null": True}


class Product(models.Model):
    """
    Представляет класс Продукт
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Продукт",
        help_text="Введите наименование продукта",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание продукта", **NULLABLE
    )
    preview = models.ImageField(
        upload_to="catalog/preview",
        **NULLABLE,
        verbose_name="Изображение",
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
            to="Category",
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Категория",
        help_text="Введите категорию продукта",
        #  у породы будет неявный параметр собаки, т к у одной породы
        #  может быть много собак
        related_name="products",
    )

    price = models.IntegerField(
        verbose_name="Цена за покупку", help_text="Введите цену за покупку"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания (записи в БД)"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения (записи в БД)"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"



class Category(models.Model):
    """
    Представляет класс Категория
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание категории", **NULLABLE
    )

    def __str__(self):
        """
        Строковое представление класса Категория
        """
        return f"{self.name}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"





class Version(models.Model):
    version_number = models.IntegerField(verbose_name="номер версии")
    version_title = models.TextField(verbose_name="название версии")
    product = models.ForeignKey(
        Product,
        related_name="versions",
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="продукт"
    )
    is_active = models.BooleanField(default=False, verbose_name="признак текущей версии")
    # version_sign = models.BooleanField(default=False, verbose_name='признак версии')
    def __str__(self):
        return f"Версия {self.version_title} номер {self.version_number}."

    class Meta:
        verbose_name = "версия"
        verbose_name_plural = "версии"

