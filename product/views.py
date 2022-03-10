from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.base import View
from .models import Product, Category, Rating, ImageHome
from .forms import ReviewForm, RatingForm
from .service import get_client_ip, get_session_key, range_date
from django_product.settings import ITEM_IN_PAGE, COUNT_DAY


class IndexView(ListView):
    """главная"""
    model = ImageHome
    queryset = ImageHome.objects.filter(draft=True).order_by('-id')
    template_name = "product/index.html"


class AboutView(TemplateView):
    template_name = "product/about.html"


class CategoryListView(ListView):
    """Список категорий"""
    model = Category
    paginate_by = ITEM_IN_PAGE
    template_name = "product/category.html"
    allow_empty = False
    context_object_name = 'categories'

    def get_queryset(self):
        category = Category.objects.all()
        return category


class ProductView(ListView):
    """Список продуктов"""
    model = Product
    paginate_by = ITEM_IN_PAGE
    template_name = "product/product_list.html"
    allow_empty = True
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
            context["rating"] = Rating.objects.get(product__slug=self.kwargs['slug'],
                                                   session_key=get_session_key(self.request)).star.value
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
    paginate_by = ITEM_IN_PAGE
    template_name = "product/product_search.html"
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        context["elements"] = Product.objects.filter(title__icontains=self.request.GET.get("q")).count()
        return context


class NewProductDay(ListView):
    """вывод новинок по дате"""
    model = Product
    paginate_by = ITEM_IN_PAGE
    template_name = "product/new_product_list.html"
    allow_empty = True
    context_object_name = 'products'

    def get_queryset(self):
        product = Product.objects.filter(draft=True, created=self.kwargs['date']).order_by('-id')
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["elements"] = Product.objects.filter(draft=True, created=self.kwargs['date']).order_by('-id').count()
        context["date"] = self.kwargs['date']
        return context


class NewProductAll(ListView):
    """вывод всех новинок"""
    model = Product
    paginate_by = ITEM_IN_PAGE
    template_name = "product/new_product_list.html"
    context_object_name = 'products'

    def get_queryset(self):
        new_date = range_date()
        return Product.objects.filter(draft=True, created__range=[new_date[0], new_date[1]]).order_by('-id')

    def get_context_data(self, **kwargs):
        new_date = range_date()
        context = super().get_context_data(**kwargs)
        context["elements"] = Product.objects.filter(draft=True, created__range=[new_date[0],
                                                                                 new_date[1]]).order_by('-id').count()
        context["date"] = f'за {COUNT_DAY} дней'
        return context
