from django.contrib import admin
from .models import News
from django.utils.safestring import mark_safe


# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "get_image", "draft",)
    list_display_links = ("title",)
    list_editable = ("draft",)


    prepopulated_fields = {"slug": ("title",)}

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.poster.url}" width="50" height="auto">')

    get_image.short_description = "Миниатюра"
    readonly_fields = ("get_image", )