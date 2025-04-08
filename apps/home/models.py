from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from assets.choices import LANG


class Banner(models.Model):
    language = models.CharField(_("Язык"), choices=LANG, default='ru', max_length=25)
    image = models.ImageField(_("Изображение"), upload_to='banners/')
    title = models.CharField(_('Название'), max_length=255, null=True, blank=True)
    slug = models.SlugField('СЛАГ', editable=False, unique=True)
    description = models.TextField(_('Текст'), null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Баннер")
        verbose_name_plural = _("Баннеры")

class PopularDirection(models.Model):
    language = models.CharField(_("Язык"), choices=LANG, default='ru', max_length=25)
    name = models.CharField(_("Город"), max_length=255)
    slug = models.SlugField('СЛАГ', editable=False, unique=True)
    image = models.ImageField(_("Изображение"), upload_to="directions/")

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Популярная направления'
        verbose_name_plural = 'Популярные направлении'


class Category(models.Model):
    language = models.CharField(_("Язык"), choices=LANG, default='ru', max_length=255)
    title = models.CharField(_('Название'), max_length=255)
    slug = models.SlugField('СЛАГ',editable=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Информация в главном экране'
        verbose_name_plural = 'Информации в главном экране'


class SubCategory(models.Model):
    cat = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='subcategory')
    title = models.CharField(_('Название'), max_length=300)
    slug = models.SlugField('СЛАГ', editable=False, unique=True, null=True, blank=True)
    description = CKEditor5Field(_('Описание'), config_name='default', blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Подкатегория информация'
        verbose_name_plural = 'Подкатегория информации'