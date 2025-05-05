from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from references.models import (
    TransportModel, PackagingType, Service, 
    DeliveryStatus, CargoType
)


class Delivery(models.Model):
    """
    Модель доставки - основная бизнес-сущность
    
    Представляет информацию о грузоперевозке, включая:
    - время отправления и прибытия
    - расстояние
    - используемый транспорт
    - тип упаковки
    - текущий статус
    - состояние транспорта
    - тип перевозимого груза
    - предоставляемые услуги
    """
    # Технические поля
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='core_created_deliveries', 
        verbose_name='Кем создано'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='core_updated_deliveries', 
        verbose_name='Кем изменено'
    )
    
    # Основные поля
    number = models.CharField('Номер', max_length=100, unique=True)
    transport_model = models.ForeignKey(
        TransportModel, 
        on_delete=models.PROTECT, 
        verbose_name='Модель транспорта'
    )
    departure_time = models.DateTimeField('Время отправления')
    arrival_time = models.DateTimeField('Время прибытия')
    distance = models.DecimalField(
        'Дистанция (км)', 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    packaging = models.ForeignKey(
        PackagingType, 
        on_delete=models.PROTECT, 
        verbose_name='Упаковка'
    )
    status = models.ForeignKey(
        DeliveryStatus, 
        on_delete=models.PROTECT, 
        verbose_name='Статус'
    )
    
    # Дополнительные поля
    CONDITION_CHOICES = [
        ('Исправно', 'Исправно'),
        ('Неисправно', 'Неисправно'),
    ]
    condition = models.CharField(
        'Техническое состояние', 
        max_length=20, 
        choices=CONDITION_CHOICES, 
        default='Исправно'
    )
    cargo_type = models.ForeignKey(
        CargoType, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Тип груза'
    )
    media_file = models.FileField(
        'Медиа-файл', 
        upload_to='delivery_files/%Y/%m/', 
        null=True, 
        blank=True
    )
    notes = models.TextField('Примечания', blank=True, null=True)
    
    # Связь с услугами (многие ко многим)
    services = models.ManyToManyField(Service, verbose_name='Услуги', blank=True)
    
    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'
        ordering = ['-departure_time']
    
    def __str__(self):
        return f"Доставка {self.number} ({self.transport_model})"
    
    def travel_time_hours(self):
        """
        Возвращает время в пути в часах
        
        Вычисляет разницу между временем прибытия и отправления,
        переводит в часы с округлением до двух знаков после запятой.
        """
        if not self.departure_time or not self.arrival_time:
            return 0
        diff = self.arrival_time - self.departure_time
        return round(diff.total_seconds() / 3600, 2)
    travel_time_hours.short_description = 'Время в пути (ч)'
