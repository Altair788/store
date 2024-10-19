from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ContactView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, CatalogProtectedView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="catalog/product_list"),
    path("contacts/", ContactView.as_view(), name="catalog/contact"),
    path("products/<int:pk>/", cache_page(60)(ProductDetailView.as_view()), name="catalog/product_detail"),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('protected-view/', CatalogProtectedView.as_view(), name='protected_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
