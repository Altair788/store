from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("catalog.urls", "catalog"), namespace="catalog")),
    path("blog/", include(("blog.urls", "blog"), namespace="blog")),
]
