from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import (
    TransportModel, PackagingType, Service, 
    DeliveryStatus, CargoType
)
from .serializers import (
    TransportModelSerializer, PackagingTypeSerializer, ServiceSerializer,
    DeliveryStatusSerializer, CargoTypeSerializer
)


class BaseReferenceViewSet(viewsets.ModelViewSet):
    """
    Базовый класс для представлений справочников
    
    Определяет общую функциональность для всех справочников:
    - фильтрация по полю active
    - поиск по name, code, description
    - сортировка по name, code
    - фильтрация по активности для не-админов
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    ordering = ['name']
    
    def get_queryset(self):
        """
        Возвращает только активные записи для не-администраторов
        
        Для пользователей с правами администратора возвращаются все записи справочника.
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # Админы видят все записи
        if user.is_staff:
            return queryset
            
        # Остальные видят только активные
        return queryset.filter(active=True)


class TransportModelViewSet(BaseReferenceViewSet):
    """
    API для управления справочником моделей транспорта
    
    Позволяет создавать, получать, обновлять и удалять записи о моделях транспорта.
    """
    queryset = TransportModel.objects.all()
    serializer_class = TransportModelSerializer


class PackagingTypeViewSet(BaseReferenceViewSet):
    """
    API для управления справочником типов упаковки
    
    Позволяет создавать, получать, обновлять и удалять записи о типах упаковки.
    """
    queryset = PackagingType.objects.all()
    serializer_class = PackagingTypeSerializer


class ServiceViewSet(BaseReferenceViewSet):
    """
    API для управления справочником услуг
    
    Позволяет создавать, получать, обновлять и удалять записи об услугах.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class DeliveryStatusViewSet(BaseReferenceViewSet):
    """
    API для управления справочником статусов доставки
    
    Позволяет создавать, получать, обновлять и удалять записи о статусах доставки.
    """
    queryset = DeliveryStatus.objects.all()
    serializer_class = DeliveryStatusSerializer


class CargoTypeViewSet(BaseReferenceViewSet):
    """
    API для управления справочником типов груза
    
    Позволяет создавать, получать, обновлять и удалять записи о типах груза.
    """
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer
