from django.contrib import admin
from .models import (
    TransportModel, PackagingType, Service, 
    DeliveryStatus, CargoType
)


class BaseReferenceAdmin(admin.ModelAdmin):
    """
    Базовый класс администрирования для справочников
    
    Определяет общие поля и функциональность для всех справочников.
    """
    list_display = ('name', 'code', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'code', 'description')
    ordering = ('name',)
    readonly_fields = ('id',)
    list_editable = ('active',)


@admin.register(TransportModel)
class TransportModelAdmin(BaseReferenceAdmin):
    """
    Администрирование моделей транспорта
    """
    pass


@admin.register(PackagingType)
class PackagingTypeAdmin(BaseReferenceAdmin):
    """
    Администрирование типов упаковки
    """
    pass


@admin.register(Service)
class ServiceAdmin(BaseReferenceAdmin):
    """
    Администрирование услуг
    """
    pass


@admin.register(DeliveryStatus)
class DeliveryStatusAdmin(BaseReferenceAdmin):
    """
    Администрирование статусов доставки
    """
    pass


@admin.register(CargoType)
class CargoTypeAdmin(BaseReferenceAdmin):
    """
    Администрирование типов груза
    """
    pass
