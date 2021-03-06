from django.shortcuts import render
from django.views.generic import View, ListView
from django_product.settings import ITEM_IN_PAGE
from .models import News


class NewsView(ListView):
    """Новости"""
    
    model = News
    paginate_by = ITEM_IN_PAGE
    allow_empty = True
    context_object_name = 'news_list'
    template_name = "product/news_list.html"

    def get_queryset(self):
        news = News.objects.filter(draft=True).order_by('-dateAdd')
        return news


class NewsDetailView(View):
    """Детали Новости"""
    
    def get(self, request, slug):
        news = News.objects.get(slug=slug)
        return render(request, "product/news_detail.html", {"news": news})
