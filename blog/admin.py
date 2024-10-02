from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "created_at",
        "updated_at",
        "preview",
        "is_published",
        "views_counter",
    )
    list_filter = ("is_published", "created_at", "views_counter",)
    search_fields = (
        "title",
        "body",
    )
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
