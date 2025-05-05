from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg, Sum, Min, Max
from django.utils import timezone
from datetime import timedelta

import datetime as dt

from .models import (
    TransportModel, PackagingType, Service, 
    DeliveryStatus, CargoType, Delivery
)
from .serializers import (
    TransportModelSerializer, PackagingTypeSerializer, ServiceSerializer,
    DeliveryStatusSerializer, CargoTypeSerializer, 
    DeliveryListSerializer, DeliveryDetailSerializer, DeliveryCreateUpdateSerializer
)


class TransportModelViewSet(viewsets.ModelViewSet):
    """API для справочника моделей транспорта"""
    queryset = TransportModel.objects.all()
    serializer_class = TransportModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    ordering = ['name']
    
    def get_queryset(self):
        """По умолчанию возвращаем только активные записи для не-админов"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Админы видят все записи
        if user.is_staff:
            return queryset
            
        # Остальные видят только активные
        return queryset.filter(active=True)


class PackagingTypeViewSet(viewsets.ModelViewSet):
    """API для справочника типов упаковки"""
    queryset = PackagingType.objects.all()
    serializer_class = PackagingTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    ordering = ['name']
    
    def get_queryset(self):
        """По умолчанию возвращаем только активные записи для не-админов"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Админы видят все записи
        if user.is_staff:
            return queryset
            
        # Остальные видят только активные
        return queryset.filter(active=True)


class ServiceViewSet(viewsets.ModelViewSet):
    """API для справочника услуг"""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    ordering = ['name']
    
    def get_queryset(self):
        """По умолчанию возвращаем только активные записи для не-админов"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Админы видят все записи
        if user.is_staff:
            return queryset
            
        # Остальные видят только активные
        return queryset.filter(active=True)


class DeliveryStatusViewSet(viewsets.ModelViewSet):
    """API для справочника статусов доставки"""
    queryset = DeliveryStatus.objects.all()
    serializer_class = DeliveryStatusSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    ordering = ['name']
    
    def get_queryset(self):
        """По умолчанию возвращаем только активные записи для не-админов"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Админы видят все записи
        if user.is_staff:
            return queryset
            
        # Остальные видят только активные
        return queryset.filter(active=True)


class CargoTypeViewSet(viewsets.ModelViewSet):
    """API для справочника типов груза"""
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    ordering = ['name']
    
    def get_queryset(self):
        """По умолчанию возвращаем только активные записи для не-админов"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Админы видят все записи
        if user.is_staff:
            return queryset
            
        # Остальные видят только активные
        return queryset.filter(active=True)


class DeliveryViewSet(viewsets.ModelViewSet):
    """API для управления доставками"""
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
        """Выбираем сериализатор в зависимости от действия"""
        if self.action in ['create', 'update', 'partial_update']:
            return DeliveryCreateUpdateSerializer
        elif self.action == 'retrieve':
            return DeliveryDetailSerializer
        else:
            return DeliveryListSerializer
    
    def get_queryset(self):
        """Фильтрация доставок по параметрам запроса"""
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
        """Отметить доставку как выполненную"""
        delivery = self.get_object()
        
        # Получаем статус "Проведено" из справочника
        try:
            completed_status = DeliveryStatus.objects.get(code='completed')
        except DeliveryStatus.DoesNotExist:
            # Если такого статуса нет, попробуем найти по имени
            try:
                completed_status = DeliveryStatus.objects.get(Q(name__iexact='Проведено') | Q(name__iexact='Выполнено'))
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
        """Получить общую статистику по доставкам"""
        # Общая статистика
        total_deliveries = Delivery.objects.count()
        completed_deliveries = Delivery.objects.filter(
            status__name__iexact='Проведено'
        ).count()
        pending_deliveries = total_deliveries - completed_deliveries
        
        # Средняя дистанция и время в пути
        avg_distance = Delivery.objects.aggregate(avg=Avg('distance'))['avg'] or 0
        
        # Возвращаем статистику
        return Response({
            'total_deliveries': total_deliveries,
            'completed_deliveries': completed_deliveries,
            'pending_deliveries': pending_deliveries,
            'avg_distance': round(float(avg_distance), 2),
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delivery_reports(request):
    """Генерация отчетов по доставкам"""
    # Получаем параметры для отчета
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    report_type = request.query_params.get('report_type', 'daily')
    
    try:
        # Конвертируем строки в даты
        if start_date:
            start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
        else:
            # По умолчанию - последние 30 дней
            start_date = timezone.now() - timedelta(days=30)
            
        if end_date:
            end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59, tzinfo=dt.timezone.utc
            )
        else:
            end_date = timezone.now()
            
        # Базовый запрос доставок в выбранном периоде
        deliveries = Delivery.objects.filter(
            departure_time__gte=start_date,
            departure_time__lte=end_date
        )
        
        result = {}
        
        # Отчет по статусам
        status_report = deliveries.values('status__name').annotate(
            count=Count('id')
        ).order_by('-count')
        
        result['status_report'] = status_report
        
        # Отчет по моделям транспорта
        transport_report = deliveries.values('transport_model__name').annotate(
            count=Count('id'),
            total_distance=Sum('distance'),
            avg_distance=Avg('distance')
        ).order_by('-count')
        
        result['transport_report'] = transport_report
        
        # Отчет по услугам
        service_report = deliveries.values('services__name').annotate(
            count=Count('id')
        ).order_by('-count')
        
        result['service_report'] = service_report
        
        # Временной отчет 
        if report_type == 'daily':
            # Группировка по дням
            date_report = deliveries.extra(
                select={'day': "DATE(departure_time)"}
            ).values('day').annotate(
                count=Count('id')
            ).order_by('day')
        elif report_type == 'monthly':
            # Группировка по месяцам
            date_report = deliveries.extra(
                select={'month': "DATE_TRUNC('month', departure_time)"}
            ).values('month').annotate(
                count=Count('id')
            ).order_by('month')
        else:
            # Группировка по неделям
            date_report = deliveries.extra(
                select={'week': "DATE_TRUNC('week', departure_time)"}
            ).values('week').annotate(
                count=Count('id')
            ).order_by('week')
        
        result['date_report'] = date_report
        
        # Общая статистика
        result['summary'] = {
            'total': deliveries.count(),
            'total_distance': deliveries.aggregate(sum=Sum('distance'))['sum'] or 0,
            'avg_distance': deliveries.aggregate(avg=Avg('distance'))['avg'] or 0,
            'min_distance': deliveries.aggregate(min=Min('distance'))['min'] or 0,
            'max_distance': deliveries.aggregate(max=Max('distance'))['max'] or 0,
        }
        
        return Response(result)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
