from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, Reviews, ProductImage, Status, Rating, RatingStar, ImageHome
from django import forms
from mptt.admin import DraggableMPTTAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget


admin.site.register(Category, DraggableMPTTAdmin, list_display=('tree_actions', 'indented_title',),
                    list_display_links=('indented_title',), prepopulated_fields={"slug": ("name",)}
                    )


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(ImageHome)
class ImageHomeAdmin(admin.ModelAdmin):
    list_display = ("id", "get_image", "title", "draft")
    list_display_links = ("title",)
    list_editable = ("draft",)

    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="auto">')

    get_image.short_description = "Миниатюра"


admin.site.title = "Admin panel - сайта"
admin.site.site_header = "Admin panel - сайта"


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 0
    readonly_fields = ("name", "email",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="auto">')

    get_image.short_description = "Изображение"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "get_image", "category", "draft", "created", "updated",)
    list_display_links = ("title",)
    list_filter = ("category", "draft", "material",)
    search_fields = ("title", )
    save_on_top = True
    save_as = True
    actions = ['publish', 'unpublish']
    list_editable = ("draft",)
    prepopulated_fields = {"slug": ("title",)}

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="auto">')

    get_image.short_description = "Изображение"

    readonly_fields = ("get_image", "persent",)

    fieldsets = (
        ("Отображение", {
            "fields": (("draft",),),
        }),
        ("", {
            "fields": (("status",),)
        }),
        ("Название", {
            "fields": (("title",),)
        }),
        ("", {
            "fields": (("slug",),)
        }),
        ("", {
            "fields": (("category"),)
        }),
        ("Изображение", {
            "fields": (("get_image", "poster",),)
        }),
        ("Характеристики", {
            "fields": (("material",),)
        }),
        ("", {
            "fields": (("country",),)
        }),
        ("", {
            "fields": (("manufactures",),)
        }),
        ("", {
            "fields": (("packaging",),)
        }),
        ("", {
            "fields": (("size"),)
        }),
        ("", {
            "fields": (("quantity"),)
        }),
        ("Цена", {
            "fields": (("retail",),)
        }),
        ("", {
            "fields": (("sale",),)
        }),
        ("", {
            "fields": (("persent",),)
        }),
        ("Описание", {
            "fields": (("description_free",),)
        }),
        ("", {
            "fields": (("description",),)
        }),
    )

    inlines = [ProductImageInline, ReviewInline, ]

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        if row_update == 2:
            message_bit = '2 записи были обновлены'
        else:
            message_bit = f'{row_update} записей было обновлено'

        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        if row_update == 2:
            message_bit = '2 записи были обновлены'
        else:
            message_bit = f'{row_update} записей было обновлено'

        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change', )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "get_image", "product",)
    list_display_links = ("title",)
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="auto">')

    get_image.short_description = "Изображение"


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "text", "email", "product") # порядок отображения
    list_display_links = ("name",) # ссылка
    readonly_fields = ("name", "email", "product", "parent") # запретить редактировать


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "draft", "created", "updated")
    list_display_links = ("name",)


@admin.register(Rating)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "star", "ip")
    list_display_links = ("product",)


@admin.register(RatingStar)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "value", )
    list_display_links = ("value",)
