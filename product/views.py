from django.db.models.fields import related
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View

from .models import Product, Category, Rating, RatingStar, ImageHome

from .forms import ReviewForm, RatingForm
from .service import get_client_ip, get_session_key, range_date
import datetime

from django.template import RequestContext


def handler404(request, *args, **argv):
    response = response.status_code = 404
    context = {"status": response}
    return render(request, '404.html', context)


# def handler500(request, *args, **argv):
#     response = render_to_response('500.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 500
#     return response


class IndexView(ListView):
    """главная"""
    model = ImageHome
    queryset = ImageHome.objects.filter(draft=True).order_by('-id')
    template_name = "product/index.html"


class CategoryListView(ListView):
    """Список категорий"""
    model = Category
    paginate_by = 1
    template_name = "product/category.html"
    allow_empty = False
    context_object_name = 'categories'
    
    def get_queryset(self):
        category = Category.objects.all()
        return category


class ProductView(ListView):
    """Список продуктов"""
    model = Product
    paginate_by = 3
    template_name = "product/product_list.html"
    allow_empty = False
    context_object_name = 'products'
    
    def get_queryset(self):
        product = Product.objects.filter(category__slug=self.kwargs['category'], draft=True)
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(slug=self.kwargs['category'])
        context["elements"] = Product.objects.filter(category__slug=self.kwargs['category'], draft=True).count()
        return context


class ProductDetailView(DetailView):
    """Полное описание продукта"""
    model = Product
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        try:
            context["rating"] = Rating.objects.get(product__slug=self.kwargs['slug'], session_key=get_session_key(self.request)).star.value
        except:
            context["rating"] = False

        return context

    def get_queryset(self):
        product = Product.objects.filter(category__slug=self.kwargs['category'], draft=True)
        return product


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        print(request.POST)
        product = Product.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.product = product
            form.save()
            print(product.get_absolute_url())
        return redirect(product.get_absolute_url())


def add_star_rating(request):
    """Добавление рейтинга product"""
    form = RatingForm(request.POST)
    if form.is_valid():
        Rating.objects.update_or_create(
            ip=get_client_ip(request),
            session_key=get_session_key(request),
            product_id=int(request.POST.get("product")),
            defaults={'star_id': int(request.POST.get("star"))}
        )
    return HttpResponse(status=201)


class Search(ListView):
    """Поиск товара"""

    paginate_by = 1
    template_name = "product/product_search.html"
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(title__icontains=self.request.GET.get("q"))
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        context["elements"] = Product.objects.filter(title__icontains=self.request.GET.get("q")).count()
        return context


# вывод новинок по дате
class NewProductDay(ListView):
    """Список продуктов"""
    model = Product
    paginate_by = 1
    template_name = "product/new_product_list.html"
    allow_empty = False
    context_object_name = 'product_list'
    
    def get_queryset(self):
        product = Product.objects.filter(draft=True, created=self.kwargs['date']).order_by('-id')
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["elements"] = Product.objects.filter(draft=True, created=self.kwargs['date']).order_by('-id').count()
        context["date"] = self.kwargs['date']
        return context


# вывод всех новинок
class NewProductAll(ListView):
    """Список продуктов"""
    model = Product
    paginate_by = 1
    template_name = "product/new_product_list.html"
    #allow_empty = False
    context_object_name = 'product_list'

    def get_queryset(self):   
        new_date = range_date()     
        return Product.objects.filter(draft=True, created__range=[new_date[0], new_date[1]]).order_by('-id')

    def get_context_data(self, **kwargs):
        new_date = range_date()
        context = super().get_context_data(**kwargs)
        context["elements"] = Product.objects.filter(draft=True, created__range=[new_date[0], new_date[1]]).order_by('-id').count()
        context["date"] = 'за 14 дней'
        return context