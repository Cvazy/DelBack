from django.contrib import admin
from .models import *


@admin.register(TransportModel)
class TransportModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'code', 'description')
    ordering = ('name',)


@admin.register(PackagingType)
class PackagingTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'code', 'description')
    ordering = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'code', 'description')
    ordering = ('name',)


@admin.register(DeliveryStatus)
class DeliveryStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'code', 'description')
    ordering = ('name',)


@admin.register(CargoType)
class CargoTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'code', 'description')
    ordering = ('name',)


class DeliveryServicesInline(admin.TabularInline):
    model = Delivery.services.through
    extra = 1


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = (
        'number', 'transport_model', 'departure_time', 
        'arrival_time', 'travel_time_hours', 'distance', 
        'status', 'condition', 'created_at'
    )
    list_filter = ('status', 'condition', 'transport_model', 'packaging')
    search_fields = ('number', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'travel_time_hours')
    fieldsets = (
        ('Основная информация', {
            'fields': ('number', 'transport_model', 'status', 'condition')
        }),
        ('Время и расстояние', {
            'fields': ('departure_time', 'arrival_time', 'travel_time_hours', 'distance')
        }),
        ('Груз и упаковка', {
            'fields': ('packaging', 'cargo_type', 'media_file')
        }),
        ('Дополнительно', {
            'fields': ('notes',)
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
    inlines = [DeliveryServicesInline]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
