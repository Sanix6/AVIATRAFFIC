from django.contrib import admin
from django.utils.html import mark_safe
from .models import Banner, PopularDirection, Category, SubCategory

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['language', 'title', 'image', 'description']
    list_display_links = ['language', 'title']
    search_fields = ['language', 'title', 'description']
    list_filter = ['language', 'title', 'description']

@admin.register(PopularDirection)
class PopularDirectionAdmin(admin.ModelAdmin):
    list_display = ['language', 'name', 'image_display']
    list_display_links = ['language', 'name']
    search_fields = ['language', 'name']
    list_filter = ['language', 'name']

    def image_display(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return "No Image"

    image_display.short_description = 'Изображение'

class SubCategoryInline(admin.StackedInline):
    model = SubCategory
    extra = 1
    ordering = ['title']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['language', 'title']
    list_display_links = ['language', 'title']
    search_fields = ['language', 'title']
    list_filter = ['language', 'title']
    inlines = [SubCategoryInline]

