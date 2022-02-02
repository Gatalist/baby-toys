from django import template
from product.models import Category, Product, Rating, Reviews, News
# from datetime import date
import datetime


register = template.Library()


# рендеринг категорий
@register.simple_tag()
def show_menu():
    categories = Category.objects.all()
    return categories


# последние продукты на главной
@register.inclusion_tag("product/tags/last_product.html")
def get_last_product():
    all_product = Product.objects.filter(draft=True).order_by('-id')
    product = all_product[:8]
    print(product)
    return {"last_products": product}


# последние отзывы на главной
@register.inclusion_tag("product/tags/last_review.html")
def get_last_review():
    all_review = Reviews.objects.all().order_by('-id')
    review = all_review[:8]
    print(review)
    return {"last_reviews": review}


# последние отзывы на главной
@register.inclusion_tag("product/tags/last_news.html")
def get_last_news():
    all_news = News.objects.filter(draft=True).order_by('-id')
    news = all_news[:8]
    print(news)
    return {"last_news": news}


@register.simple_tag()
def get_date_list_menu():
    now_date = datetime.date.today()
    last_days = 14
    dateList = []

    for x in range (0, last_days):
        date = now_date - datetime.timedelta(days = x)
        product = Product.objects.filter(draft=True, created=date).count()

        if product > 0:
            dateList.append(str(date))

    return dateList
