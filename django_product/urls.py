from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ProductSitemap, StaticSitemap



sitemaps = {
    'product': ProductSitemap,
    'static': StaticSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("", include("product.urls")),
    path("user/", include("users.urls")),
    path("news/", include("news.urls")),
    path("contact/", include("subscribe.urls")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]


handler404 = "django_product.views.handler404"
handler500 = "django_product.views.handler500"


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
