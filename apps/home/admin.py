from django.contrib import admin
from django.utils.html import mark_safe
from .models import Banner, PopularDirection, Information, SubInformation, FAQ
from assets.forms import *

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['language', 'title', 'image', 'description']
    list_display_links = ['language', 'title']
    search_fields = ['language', 'title', 'description']
    list_filter = ['language', 'title', 'description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(PopularDirection)
class PopularDirectionAdmin(admin.ModelAdmin):
    list_display = ['language', 'name', 'image_display']
    list_display_links = ['language', 'name']
    search_fields = ['language', 'name']
    list_filter = ['language', 'name']
    prepopulated_fields = {'slug': ('name',)}

    def image_display(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return "No Image"

    image_display.short_description = 'Изображение'


class SubInfoInline(admin.StackedInline):
    model = SubInformation
    extra = 1
    ordering = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ['language', 'title']
    list_display_links = ['language', 'title']
    search_fields = ['language', 'title']
    list_filter = ['language', 'title']
    inlines = [SubInfoInline]
    prepopulated_fields = {'slug': ('title',)}


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'language']
    list_display_links = ['question', 'language']
    search_fields = ['question', 'language']
    list_filter = ['question', 'language']
    prepopulated_fields = {'slug': ('question',)}
