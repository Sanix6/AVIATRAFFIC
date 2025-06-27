from django.db import models
from django.utils.translation import gettext_lazy as _



#apps
from apps.users.models import User
from assets.choices import *

from django.db import models

class Segment(models.Model):
    company = models.CharField(
        max_length=10,
        help_text="Код авиакомпании, выполняющей рейс (например, SU, S7)"
    )
    flight = models.CharField(
        max_length=10,
        help_text="Номер рейса (например, 1234)"
    )
    departure = models.CharField(
        max_length=10,
        help_text="Код аэропорта отправления (например, SVO)"
    )
    arrival = models.CharField(
        max_length=10,
        help_text="Код аэропорта прибытия (например, JFK)"
    )
    date = models.CharField(
        max_length=20,
        help_text="Дата отправления в формате YYYY-MM-DD"
    )
    subclass = models.CharField(
        max_length=5,
        help_text="Буквенное обозначение подкласса тарифа (например, 'Y', 'E')"
    )
    joint_id = models.IntegerField(
        null=True, blank=True,
        help_text="Идентификатор объединения сегментов (если есть)"
    )

    def __str__(self):
        return f"{self.company}{self.flight} {self.departure}-{self.arrival} on {self.date}"


class Passenger(models.Model):
    lastname = models.CharField(
        max_length=100,
        help_text="Фамилия пассажира"
    )
    firstname = models.CharField(
        max_length=100,
        help_text="Имя пассажира"
    )
    surname = models.CharField(
        max_length=100,
        help_text="Отчество пассажира", 
        null=True, blank=True
    )
    category = models.CharField(
        max_length=10,
        # choices=CATEGORY_CHOICES,
        help_text="Категория пассажира: ADT (взрослый), CHD (ребёнок), INF (младенец)"
    )
    sex = models.CharField(
        max_length=10,
        # choices=SEX_CHOICES,
        help_text="Пол пассажира: M (мужской) или F (женский)"
    )
    birthdate = models.DateField(
        help_text="Дата рождения пассажира"
    )
    doc_country = models.CharField(
        max_length=25,
        # choices=COUNTRY_CHOICES
    )
    doccode = models.CharField(
        max_length=10,
        help_text="Тип документа (например, P для паспорта)"
    )
    doc = models.CharField(
        max_length=30,
        help_text="Номер документа"
    )
    pspexpire = models.DateField(
        help_text="Дата истечения срока действия удостоверения личности"
    )

    def __str__(self):
        return f"{self.lastname} {self.firstname}"


class Booking(models.Model):
    regnum = models.CharField(
        max_length=20,
        null=True, blank=True,
        help_text="Регистрационный номер бронирования во внешней системе"
    )
    agency = models.CharField(
        max_length=50,
        null=True, blank=True,
        help_text="Код или имя агентства, создавшего бронирование"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата и время создания записи о бронировании"
    )
    segments = models.ManyToManyField(
        Segment,
        related_name="bookings",
        help_text="Сегменты маршрута, входящие в бронирование"
    )
    passengers = models.ManyToManyField(
        Passenger,
        related_name="bookings",
        help_text="Пассажиры, участвующие в бронировании"
    )
    contact_phone = models.CharField(
        max_length=20,
        null=True, blank=True,
        help_text="Контактный телефон пассажира или агентства"
    )

    def __str__(self):
        return f"Booking #{self.id or 'N/A'} - {self.regnum or 'No Regnum'}"


class Countries(models.Model):
    name = models.CharField(
        _('Страна'),
        max_length=200,
        help_text="Название страны (например, Kyrgyzstan)"
    )
    code_name = models.CharField(
        _('Код страны'),
        max_length=3,
        unique=True,
        help_text="Код страны в формате ISO Alpha-3 (например, 'KGZ')"
    )
    img = models.ImageField(
        _('Флаг'),
        upload_to='countries',
        help_text="Изображение флага страны"
    )

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return f"{self.name} ({self.code_name})" if self.code_name else self.name

    def save(self, *args, **kwargs):
        self.code_name = self.code_name.upper()
        super().save(*args, **kwargs)


# class Cities(models.Model):
#     country = models.ForeignKey(
#         Countries,
#         related_name="cities",
#         on_delete=models.CASCADE,
#         verbose_name=_("Страна"),
#         help_text="Страна, к которой относится город"
#     )
#     name = models.CharField(
#         _('Город'),
#         max_length=200,
#         help_text="Название города (например, Bishkek)"
#     )
#     code_name = models.CharField(
#         _('Код города'),
#         max_length=3,
#         help_text="Код города в формате IATA (например, 'FRU')"
#     )

#     class Meta:
#         verbose_name = 'Город'
#         verbose_name_plural = 'Города'

#     def __str__(self):
#         return f"{self.name} ({self.code_name})"

#     def save(self, *args, **kwargs):
#         self.code_name = self.code_name.upper()
#         super().save(*args, **kwargs)


# class Airports(models.Model):
#     city = models.ForeignKey(
#         Cities,
#         related_name="airports",
#         on_delete=models.CASCADE,
#         verbose_name='Город',
#         help_text="Город, к которому относится аэропорт"
#     )
#     name = models.CharField(
#         _('Аэропорт'),
#         max_length=200,
#         help_text="Название аэропорта (например, Manas International Airport)"
#     )
#     code_name = models.CharField(
#         _('Код аэропорта'),
#         max_length=3,
#         help_text="Код аэропорта в формате IATA (например, 'FRU')"
#     )

#     class Meta:
#         verbose_name = 'Аэропорт'
#         verbose_name_plural = 'Аэропорты'

#     def __str__(self):
#         return f"{self.name} ({self.code_name})"

#     def save(self, *args, **kwargs):
#         self.code_name = self.code_name.upper()
#         super().save(*args, **kwargs)