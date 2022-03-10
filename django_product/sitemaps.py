from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from product.models import Product


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ['/', '/about/', '/news/', '/contact/', '/user/basket/', '/user/likes/']

    def location(self, item):
        return item


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    protocol = 'https'

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated
        
    def location(self,obj):
        return obj.get_absolute_url()
