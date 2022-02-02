from django.db import models
from datetime import date
from django.urls import reverse

from news.models import News
# from django.db.models.fields import related
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """Категории"""
    name = models.CharField(max_length=150, verbose_name="Название")
    slug = models.SlugField(max_length=250, unique=True, db_index=True, blank=True, null=True, verbose_name="url")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Категория",
                            related_name='children')
    poster = models.ImageField(upload_to="category/%Y/%m/%d/", verbose_name="Изображение")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_list", kwargs={"category": self.slug})

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name_plural = "Категории"
        verbose_name = "Категории"


class Status(models.Model):
    """Статус"""
    name = models.CharField(max_length=24, verbose_name="Имя")
    draft = models.BooleanField(default=True, verbose_name="Активен")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Product(models.Model):
    """Продукт"""
    draft = models.BooleanField(default=True, verbose_name="Показывать на сайте")
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Статус")
    title = models.CharField(max_length=250, verbose_name="Название")
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name="url")
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Категория")
    created = models.DateField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateField(auto_now=True, verbose_name="Обновлен")

    material = models.CharField(null=True, blank=True, max_length=100, verbose_name="Материал")
    country = models.CharField("Страна", null=True, blank=True, max_length=150)
    manufactures = models.CharField("Производитель", null=True, blank=True, max_length=150)
    packaging = models.CharField("Упаковка", null=True, blank=True, max_length=150)
    size = models.CharField("Размер", null=True, blank=True, max_length=150)
    quantity = models.IntegerField("В наличии", null=True, blank=True, help_text="шт.")

    retail = models.FloatField("Цена", null=True, default=0, help_text="грн.")
    sale = models.FloatField("Акция Цена", null=True, blank=True, help_text="грн.")
    persent = models.IntegerField("Скидка", null=True, blank=True, help_text="%")  # (sale / retail) -1

    description_free = models.TextField("Краткое описание", null=True, blank=True, max_length=200)
    description = models.TextField("Описание", max_length=5000)
    poster = models.ImageField("Изображение", upload_to='products/%Y/%m/%d/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"category": self.category.slug, "slug": self.slug})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def get_rating(self):
        rating = Rating.objects.filter(product_id=self.pk)
        count = rating.count()
        sum_star = 0
        star_on = []
        star_off = []
        
        if count == 0:
            star_off = ['star_off', 'star_off', 'star_off', 'star_off', 'star_off']
            return {'star_off': star_off}
        else:
            for r in rating:
                sum_star += r.star.value
        
        star = round(sum_star / count, 1)
        
        for i in range(int(star)):
            star_on.append('star_on')

        if star - len(star_on) >= 0.5:
            star_on.append('star_on')
        
        for j in range(5 - len(star_on)):
            star_off.append('star_off')
    
        return {'star_on': star_on, 'star_off': star_off, 'star': star}


    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.sale:
            num = (self.sale / self.retail) - 1
            self.persent = int(round(num, 2) * 100)
        else:
            self.persent = None

        super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    """Изображение товара"""
    title = models.CharField("Заголовок", max_length=150)
    image = models.ImageField("Изображение", upload_to='products_image/')
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображение товаров"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Отзыв', max_length=5000)
    dateAdd = models.DateField("Дата добавления", default=date.today)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True
    )

    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
    


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    session_key = models.CharField("Ключ сессии", max_length=128, blank=True, null=True, default=None)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="товар")

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class ImageHome(models.Model):
    """слайдер на главной"""
    draft = models.BooleanField("Показывать на сайте", default=True)
    title = models.CharField("Заголовок", null=True, blank=True, max_length=100)
    up_title = models.CharField("Подзаголовок", null=True, blank=True, max_length=50)
    product = models.ForeignKey(Product, verbose_name="Продукт", null=True, blank=True, on_delete=models.CASCADE)
    news = models.ForeignKey(News, verbose_name="Новость", null=True, blank=True, on_delete=models.CASCADE)
    slug = models.CharField("url", null=True, blank=True, max_length=250)
    btn_name = models.CharField("Текст на кнопке", null=True, blank=True, default='Подробнее', max_length=50)
    image = models.ImageField("Изображение", upload_to="slider/%Y/%m/%d/")
    
    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды на главной"
