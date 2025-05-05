from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Delivery
from references.serializers import ServiceSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователей системы
    
    Используется для представления информации о создателе/редакторе доставки
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class DeliveryListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка доставок с минимумом полей
    
    Используется при выводе доставок в списке для улучшения производительности.
    Содержит только основные поля, необходимые для отображения в таблице.
    """
    transport_model_name = serializers.CharField(source='transport_model.name', read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)
    packaging_name = serializers.CharField(source='packaging.name', read_only=True)
    travel_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Delivery
        fields = (
            'id', 'number', 'transport_model', 'transport_model_name',
            'departure_time', 'arrival_time', 'travel_time',
            'distance', 'status', 'status_name', 
            'condition', 'packaging', 'packaging_name'
        )
    
    def get_travel_time(self, obj):
        """
        Возвращает время в пути в часах
        """
        return obj.travel_time_hours()


class DeliveryDetailSerializer(serializers.ModelSerializer):
    """
    Подробный сериализатор для доставки
    
    Включает все поля и связанные данные для детального просмотра доставки.
    """
    transport_model_name = serializers.CharField(source='transport_model.name', read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)
    packaging_name = serializers.CharField(source='packaging.name', read_only=True)
    cargo_type_name = serializers.CharField(source='cargo_type.name', read_only=True, allow_null=True)
    services_data = ServiceSerializer(source='services', many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    updated_by_name = serializers.CharField(source='updated_by.username', read_only=True, allow_null=True)
    travel_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Delivery
        fields = '__all__'
        extra_fields = (
            'transport_model_name', 'status_name', 'packaging_name', 
            'cargo_type_name', 'services_data', 'created_by_name', 
            'updated_by_name', 'travel_time'
        )
    
    def get_travel_time(self, obj):
        """
        Возвращает время в пути в часах
        """
        return obj.travel_time_hours()


class DeliveryCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания/обновления доставки
    
    Используется при создании новой доставки или обновлении существующей.
    Содержит валидацию данных и логику сохранения информации о пользователе.
    """
    class Meta:
        model = Delivery
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    def validate(self, data):
        """
        Проверяет корректность времени доставки
        
        Время прибытия должно быть позже времени отправления.
        """
        if 'departure_time' in data and 'arrival_time' in data:
            if data['departure_time'] >= data['arrival_time']:
                raise serializers.ValidationError({
                    'arrival_time': 'Время прибытия должно быть позже времени отправления'
                })
        
        return data
    
    def create(self, validated_data):
        """
        Создает доставку и добавляет информацию о пользователе-создателе
        """
        services = validated_data.pop('services', [])
        request = self.context.get("request")
        user = request.user if request else None
        
        delivery = Delivery.objects.create(**validated_data, created_by=user, updated_by=user)
        
        if services:
            delivery.services.set(services)
            
        return delivery
    
    def update(self, instance, validated_data):
        """
        Обновляет доставку и фиксирует пользователя, выполнившего обновление
        """
        services = validated_data.pop('services', None)
        request = self.context.get("request")
        user = request.user if request else None
        
        # Обновляем все поля, кроме ManyToMany
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Обновляем информацию о том, кто последним изменил
        instance.updated_by = user
        instance.save()
        
        # Обновляем ManyToMany связи, если они были в запросе
        if services is not None:
            instance.services.set(services)
            
        return instance 