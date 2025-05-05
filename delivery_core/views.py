from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone

from .models import Delivery
from .serializers import (
    DeliveryListSerializer, DeliveryDetailSerializer, DeliveryCreateUpdateSerializer
)
from references.models import DeliveryStatus


class DeliveryViewSet(viewsets.ModelViewSet):
    """
    API для управления доставками
    
    Предоставляет функционал для создания, чтения, обновления и удаления доставок.
    Поддерживает фильтрацию, поиск и сортировку данных.
    """
    queryset = Delivery.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'transport_model', 'status', 'packaging', 
        'condition', 'cargo_type'
    ]
    search_fields = ['number', 'notes']
    ordering_fields = [
        'number', 'departure_time', 'arrival_time', 
        'distance', 'created_at', 'updated_at'
    ]
    ordering = ['-departure_time']
    
    def get_serializer_class(self):
        """
        Выбирает сериализатор в зависимости от действия
        
        Для детального просмотра используется DetailSerializer.
        Для создания и обновления используется CreateUpdateSerializer.
        Для списка используется облегченный ListSerializer.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return DeliveryCreateUpdateSerializer
        elif self.action == 'retrieve':
            return DeliveryDetailSerializer
        else:
            return DeliveryListSerializer
    
    def get_queryset(self):
        """
        Фильтрация доставок по параметрам запроса
        
        Поддерживаемые фильтры:
        - min_distance, max_distance: диапазон расстояний
        - services: список ID предоставляемых услуг
        - time_filter: фильтр по времени (today, week)
        """
        queryset = super().get_queryset()
        
        # Фильтр по диапазону дистанций
        min_distance = self.request.query_params.get('min_distance', None)
        max_distance = self.request.query_params.get('max_distance', None)
        
        if min_distance:
            queryset = queryset.filter(distance__gte=float(min_distance))
        if max_distance:
            queryset = queryset.filter(distance__lte=float(max_distance))
        
        # Фильтр по услугам
        services = self.request.query_params.get('services', None)
        if services:
            service_ids = [int(s) for s in services.split(',')]
            queryset = queryset.filter(services__id__in=service_ids).distinct()
        
        # Фильтр по времени
        time_filter = self.request.query_params.get('time_filter', None)
        if time_filter:
            now = timezone.now()
            if time_filter == 'today':
                today_start = timezone.now().replace(hour=0, minute=0, second=0)
                queryset = queryset.filter(departure_time__gte=today_start)
            elif time_filter == 'week':
                week_ago = now - timezone.timedelta(days=7)
                queryset = queryset.filter(departure_time__gte=week_ago)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """
        Отметить доставку как выполненную
        
        Устанавливает доставке статус "Проведено" или "Выполнено".
        Если такого статуса нет в справочнике, возвращает ошибку.
        """
        delivery = self.get_object()
        
        # Получаем статус "Проведено" из справочника
        try:
            completed_status = DeliveryStatus.objects.get(code='completed')
        except DeliveryStatus.DoesNotExist:
            # Если такого статуса нет, попробуем найти по имени
            try:
                completed_status = DeliveryStatus.objects.get(
                    Q(name__iexact='Проведено') | Q(name__iexact='Выполнено')
                )
            except DeliveryStatus.DoesNotExist:
                return Response({
                    "error": "Статус 'Проведено' не найден в справочнике"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        delivery.status = completed_status
        delivery.updated_by = request.user
        delivery.save()
        
        serializer = DeliveryDetailSerializer(delivery)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Получить общую статистику по доставкам
        
        Возвращает:
        - общее количество доставок
        - количество выполненных доставок
        - количество ожидающих доставок
        - среднюю дистанцию
        """
        # Общая статистика
        total_deliveries = Delivery.objects.count()
        completed_deliveries = Delivery.objects.filter(
            status__name__iexact='Проведено'
        ).count()
        pending_deliveries = total_deliveries - completed_deliveries
        
        # Средняя дистанция
        from django.db.models import Avg
        avg_distance = Delivery.objects.aggregate(avg=Avg('distance'))['avg'] or 0
        
        # Возвращаем статистику
        return Response({
            'total_deliveries': total_deliveries,
            'completed_deliveries': completed_deliveries,
            'pending_deliveries': pending_deliveries,
            'avg_distance': round(float(avg_distance), 2),
        })
