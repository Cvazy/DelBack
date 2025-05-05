from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class TransportModel(models.Model):
    """Справочник моделей транспорта"""
    name = models.CharField('Название', max_length=100)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True, null=True)
    active = models.BooleanField('Активно', default=True)
    
    class Meta:
        verbose_name = 'Модель транспорта'
        verbose_name_plural = 'Модели транспорта'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class PackagingType(models.Model):
    """Справочник типов упаковки"""
    name = models.CharField('Название', max_length=100)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True, null=True)
    active = models.BooleanField('Активно', default=True)
    
    class Meta:
        verbose_name = 'Тип упаковки'
        verbose_name_plural = 'Типы упаковки'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Service(models.Model):
    """Справочник услуг"""
    name = models.CharField('Название', max_length=100)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True, null=True)
    active = models.BooleanField('Активно', default=True)
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class DeliveryStatus(models.Model):
    """Справочник статусов доставки"""
    name = models.CharField('Название', max_length=100)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True, null=True)
    active = models.BooleanField('Активно', default=True)
    
    class Meta:
        verbose_name = 'Статус доставки'
        verbose_name_plural = 'Статусы доставки'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CargoType(models.Model):
    """Справочник типов груза (опционально)"""
    name = models.CharField('Название', max_length=100)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True, null=True)
    active = models.BooleanField('Активно', default=True)
    
    class Meta:
        verbose_name = 'Тип груза'
        verbose_name_plural = 'Типы груза'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Delivery(models.Model):
    """Модель доставки - основная бизнес-сущность"""
    # Технические поля
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='created_deliveries', verbose_name='Кем создано')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='updated_deliveries', verbose_name='Кем изменено')
    
    # Основные поля
    number = models.CharField('Номер', max_length=100, unique=True)
    transport_model = models.ForeignKey(TransportModel, on_delete=models.PROTECT, 
                                      verbose_name='Модель транспорта')
    departure_time = models.DateTimeField('Время отправления')
    arrival_time = models.DateTimeField('Время прибытия')
    distance = models.DecimalField('Дистанция (км)', max_digits=10, decimal_places=2,
                                 validators=[MinValueValidator(0)])
    packaging = models.ForeignKey(PackagingType, on_delete=models.PROTECT, 
                                verbose_name='Упаковка')
    status = models.ForeignKey(DeliveryStatus, on_delete=models.PROTECT, 
                             verbose_name='Статус')
    
    # Дополнительные поля
    CONDITION_CHOICES = [
        ('Исправно', 'Исправно'),
        ('Неисправно', 'Неисправно'),
    ]
    condition = models.CharField('Техническое состояние', max_length=20, 
                               choices=CONDITION_CHOICES, default='Исправно')
    cargo_type = models.ForeignKey(CargoType, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Тип груза')
    media_file = models.FileField('Медиа-файл', upload_to='delivery_files/%Y/%m/', 
                                null=True, blank=True)
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
        """Возвращает время в пути в часах"""
        if not self.departure_time or not self.arrival_time:
            return 0
        diff = self.arrival_time - self.departure_time
        return round(diff.total_seconds() / 3600, 2)
    travel_time_hours.short_description = 'Время в пути (ч)'
