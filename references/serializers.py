from rest_framework import serializers
from .models import (
    TransportModel, PackagingType, Service, 
    DeliveryStatus, CargoType
)


class BaseReferenceSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для справочников
    
    Содержит общую логику для всех справочников.
    """
    class Meta:
        fields = '__all__'


class TransportModelSerializer(BaseReferenceSerializer):
    """
    Сериализатор для моделей транспорта
    """
    class Meta(BaseReferenceSerializer.Meta):
        model = TransportModel


class PackagingTypeSerializer(BaseReferenceSerializer):
    """
    Сериализатор для типов упаковки
    """
    class Meta(BaseReferenceSerializer.Meta):
        model = PackagingType


class ServiceSerializer(BaseReferenceSerializer):
    """
    Сериализатор для услуг
    """
    class Meta(BaseReferenceSerializer.Meta):
        model = Service


class DeliveryStatusSerializer(BaseReferenceSerializer):
    """
    Сериализатор для статусов доставки
    """
    class Meta(BaseReferenceSerializer.Meta):
        model = DeliveryStatus


class CargoTypeSerializer(BaseReferenceSerializer):
    """
    Сериализатор для типов груза
    """
    class Meta(BaseReferenceSerializer.Meta):
        model = CargoType 