from django.db import models
from django.utils.translation import gettext_lazy as _

class Airports(models.Model):
    name = models.CharField(_('Аэропрт'), max_length=200)
    code_name = models.CharField(_('Код аэропорта'), max_length=3, help_text='FRU')

    class Meta:
        verbose_name = 'Аэропорт'
        verbose_name_plural = 'Аэропорты'

    def save(self, *args, **kwargs):
        self.code_name = self.code_name.upper()
        super().save(*args, **kwargs)


class Cities(models.Model):
    aero = models.ForeignKey(Airports, related_name="aero", on_delete=models.CASCADE, verbose_name='Аеропорт')
    name = models.CharField(_('Город'), max_length=200)
    code_name = models.CharField(_('Код города'), max_length=3, help_text='FRU')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def save(self, *args, **kwargs):
        self.code_name = self.code_name.upper()
        super().save(*args, **kwargs)


class Countries(models.Model):
    cities = models.ForeignKey(Cities, related_name="cities", on_delete=models.CASCADE, verbose_name=_("Город"))
    name = models.CharField(_('Страна'), max_length=200)
    code_name = models.CharField(_('Код страны'), max_length=3, unique=True)
    img = models.ImageField(_('Флаг'), upload_to='countries')

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        if self.code_name:
            return f"{self.name}-{self.code_name}"
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.code_name = self.code_name.upper()
        super().save(*args, **kwargs)
