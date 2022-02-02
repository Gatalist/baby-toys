from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("product.urls")),
    path("user/", include("users.urls")),
    path("news/", include("news.urls")),
    path("contact/", include("subscribe.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
