from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Count, Avg, Sum, Min, Max
from datetime import timedelta
import datetime as dt

from delivery_core.models import Delivery


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delivery_reports(request):
    """
    Генерация отчетов по доставкам
    
    Предоставляет различные статистические отчеты по доставкам за указанный период:
    - распределение по статусам
    - использование моделей транспорта
    - популярность услуг
    - временное распределение доставок

    Параметры:
    - start_date: начальная дата периода (YYYY-MM-DD)
    - end_date: конечная дата периода (YYYY-MM-DD)
    - report_type: тип группировки по времени (daily, weekly, monthly)
    
    Если даты не указаны, по умолчанию используется период 30 дней до текущей даты.
    """
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
