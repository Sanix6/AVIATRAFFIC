from django.contrib import admin
from django.utils.html import format_html
from .models import *


@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_img']
    list_display_links = ['id', 'name', 'get_img']

    def get_img(self, obj):
        if obj.img:
            return format_html(f"<img src='{obj.img.url}' height='60' width='100'>")

    get_img.short_description = 'Изображение'


class AirportsInline(admin.StackedInline):
    model = Airports
    extra = 1

@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    inlines = [AirportsInline]
    list_display = ['country', 'name', 'code_name']
