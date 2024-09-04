from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import contact, products_list, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path("", products_list, name="main/products_list"),
    path("contacts/", contact, name="main/contact"),
    path("products/<int:pk>/", product_detail, name="main/product_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
