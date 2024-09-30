from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ContactView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="catalog/product_list"),
    path("contacts/", ContactView.as_view(), name="catalog/contact"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="catalog/product_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
