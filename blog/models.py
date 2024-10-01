from django.db import models

NULLABLE = {"blank": True, "null": True}


class Article(models.Model):
    """
    It represents the class Article
    """
    title = models.CharField(
        max_length=150,
        verbose_name='заголовок',
        help_text='Введите заголовок статьи'
    )
    slug = models.CharField(
        max_length=150,
        verbose_name='slug',
        null=True,
        blank=True
    )
    body = models.TextField(
        verbose_name='содержимое'
    )
    preview = models.ImageField(
        upload_to="blog/preview",
        **NULLABLE,
        verbose_name="изображение",
        help_text="Загрузите изображение (обложку) для статьи"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания (записи в БД)"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения (записи в БД)"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='опубликована'
    )
    views_counter = models.PositiveIntegerField(
        verbose_name="счетчик просмотров",
        help_text="Укажите количество просмотров",
        default=0
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
