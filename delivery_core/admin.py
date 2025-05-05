from django.contrib import admin
from .models import Delivery


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    """
    Администрирование доставок
    
    Предоставляет интерфейс для управления доставками через админ-панель Django.
    """
    list_display = (
        'number', 'transport_model', 'status', 
        'departure_time', 'arrival_time', 'travel_time_hours',
        'distance', 'condition'
    )
    list_filter = ('status', 'condition', 'transport_model', 'cargo_type')
    search_fields = ('number', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    filter_horizontal = ('services',)
    date_hierarchy = 'departure_time'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('number', 'transport_model', 'status')
        }),
        ('Время и расстояние', {
            'fields': ('departure_time', 'arrival_time', 'distance')
        }),
        ('Груз и упаковка', {
            'fields': ('packaging', 'cargo_type', 'condition')
        }),
        ('Дополнительная информация', {
            'fields': ('services', 'media_file', 'notes')
        }),
        ('Служебная информация', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Сохраняет информацию о пользователе при создании/изменении
        """
        if not change:  # Если создание новой записи
            obj.created_by = request.user
        
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
