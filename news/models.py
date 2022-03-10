from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from datetime import date
from django.urls import reverse


class News(models.Model):
    """Новости"""
    draft = models.BooleanField("Показывать на сайте", default=False)
    title = models.CharField("Название", max_length=250)
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name="url")
    dateAdd = models.DateField("Дата добавления", default=date.today)
    description_free = models.TextField("Короткий текст публикации", max_length=250, default=" ")
    description = RichTextUploadingField("Текст публикации")
    poster = models.ImageField("Изображение", upload_to='news/%Y/%m/%d/')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
