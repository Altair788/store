from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contact

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="main/home"),
    path("contacts/", contact, name="main/contact"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
