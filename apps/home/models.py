from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from assets.choices import LANG

class Banner(models.Model):
    language = models.CharField(_("Язык"), choices=LANG, default='ru', max_length=25)
    image = models.ImageField(_("Изображение"), upload_to='banners/')
    title = models.CharField(_('Название'), max_length=255, null=True, blank=True)
    slug = models.SlugField('СЛАГ', unique=True, blank=True)
    description = models.TextField(_('Текст'), null=True, blank=True)

    class Meta:
        verbose_name = _("Баннер")
        verbose_name_plural = _("Баннеры")

class PopularDirection(models.Model):
    language = models.CharField(_("Язык"), choices=LANG, default='ru', max_length=25)
    name = models.CharField(_("Город"), max_length=255)
    slug = models.SlugField('СЛАГ', unique=True, blank=True)
    image = models.ImageField(_("Изображение"), upload_to="directions/")

    class Meta:
        verbose_name = 'Популярная направления'
        verbose_name_plural = 'Популярные направлении'


class Information(models.Model):
    language = models.CharField(_("Язык"), choices=LANG, default='ru', max_length=255)
    title = models.CharField(_('Название'), max_length=255)
    slug = models.SlugField('СЛАГ', unique=True, blank=True)
    img = models.ImageField('Логотип', upload_to='informations/')
    background_color = models.CharField(
        'Цвет фона', max_length=20, default='#ffffff',
        help_text='Например, #f0f8ff, red, rgb(255,255,255)', null=True, blank=True
    )
    description = RichTextUploadingField(_('Информация'), config_name='default', blank=True, null=True)
    

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Информация'
        verbose_name_plural = 'Информации'


class SubInformation(models.Model):
    cat = models.ForeignKey(to=Information, on_delete=models.CASCADE, verbose_name='Категория', related_name='subinfo')
    title = models.CharField(_('Название'), max_length=300)
    subject = models.CharField(_('Cодержимое'), max_length=255, null=True, blank=True)
    slug = models.SlugField('СЛАГ', unique=True, blank=True)
    description = RichTextUploadingField(_('Информация'), config_name='default', blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Подкатегория информация'
        verbose_name_plural = 'Подкатегория информации'


class FAQ(models.Model):
    language = models.CharField(_("Язык"), choices=LANG, default='ru', max_length=255)
    slug = models.SlugField('СЛАГ', unique=True, blank=True)
    question = models.CharField(_('Вопрос'), max_length=255)
    answer = RichTextUploadingField(_('Ответ'),config_name='default')

    class Meta:
        verbose_name = 'Частые вопросы'
        verbose_name_plural = 'Частые вопросы'
