from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ContactView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, CatalogProtectedView, CategoryListView, CategoryDetailView

app_name = CatalogConfig.name


urlpatterns = [
    path("", never_cache(ProductListView.as_view()), name="catalog/product_list"),
    path('categories/', CategoryListView.as_view(), name='catalog/category_list'),
    path("contacts/", ContactView.as_view(), name="catalog/contact"),
    path("products/<int:pk>/", cache_page(60)(ProductDetailView.as_view()), name="catalog/product_detail"),
    path("categories/<int:pk>/", cache_page(60)(CategoryDetailView.as_view()), name="catalog/category_detail"),
    path('create/', never_cache(ProductCreateView.as_view()), name='create_product'),
    path('update/<int:pk>/', never_cache(ProductUpdateView.as_view()), name='update_product'),
    path('delete/<int:pk>/', never_cache(ProductDeleteView.as_view()), name='delete_product'),
    path('protected-view/', CatalogProtectedView.as_view(), name='protected_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
