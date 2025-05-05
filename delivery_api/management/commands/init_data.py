from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from delivery_api.models import (
    TransportModel, PackagingType, Service, 
    DeliveryStatus, CargoType, Delivery
)
from django.utils import timezone
import random
from decimal import Decimal
from datetime import timedelta


class Command(BaseCommand):
    help = 'Инициализация базы данных начальными данными'

    def handle(self, *args, **options):
        self.stdout.write('Инициализация данных...')
        
        # Создаем админа, если его нет
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Пользователь admin создан'))
        
        # Создаем начальные справочники
        self._create_transport_models()
        self._create_packaging_types()
        self._create_services()
        self._create_delivery_statuses()
        self._create_cargo_types()
        
        # Создаем тестовые доставки, если их нет
        if Delivery.objects.count() == 0:
            self._create_sample_deliveries()
        
        self.stdout.write(self.style.SUCCESS('Инициализация данных завершена!'))
    
    def _create_transport_models(self):
        """Создание справочника моделей транспорта"""
        models = [
            {'name': 'V01', 'code': 'v01', 'description': 'Грузовой фургон V01'},
            {'name': 'X20', 'code': 'x20', 'description': 'Легкий грузовик X20'},
            {'name': 'REX', 'code': 'rex', 'description': 'Тяжелый грузовик REX'},
            {'name': 'Спринтер', 'code': 'sprinter', 'description': 'Mercedes Sprinter'},
            {'name': 'Газель', 'code': 'gazel', 'description': 'ГАЗель Next'},
            {'name': 'Лада Груз', 'code': 'lada', 'description': 'Лада ларгус фургон'},
            {'name': 'ЭлектроМобиль', 'code': 'electro', 'description': 'Электрический фургон'},
        ]
        
        for model_data in models:
            TransportModel.objects.get_or_create(
                code=model_data['code'],
                defaults={
                    'name': model_data['name'],
                    'description': model_data['description'],
                    'active': True,
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(models)} моделей транспорта'))
    
    def _create_packaging_types(self):
        """Создание справочника типов упаковки"""
        packaging_types = [
            {'name': 'Пакет до 1 кг', 'code': 'packet_1kg', 'description': 'Пакет для лёгких грузов до 1 кг'},
            {'name': 'Целофан', 'code': 'cellophane', 'description': 'Целофановая упаковка'},
            {'name': 'Коробка', 'code': 'box', 'description': 'Обычная картонная коробка'},
            {'name': 'Бумажный пакет', 'code': 'paper_bag', 'description': 'Экологичный бумажный пакет'},
            {'name': 'Пластиковый контейнер', 'code': 'plastic_container', 'description': 'Пластиковый контейнер с крышкой'},
            {'name': 'Ящик', 'code': 'crate', 'description': 'Деревянный или пластиковый ящик'},
            {'name': 'Нет упаковки', 'code': 'no_packaging', 'description': 'Без упаковки'},
        ]
        
        for type_data in packaging_types:
            PackagingType.objects.get_or_create(
                code=type_data['code'],
                defaults={
                    'name': type_data['name'],
                    'description': type_data['description'],
                    'active': True,
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(packaging_types)} типов упаковки'))
    
    def _create_services(self):
        """Создание справочника услуг"""
        services = [
            {'name': 'До клиента', 'code': 'to_client', 'description': 'Доставка непосредственно до клиента'},
            {'name': 'Перемещение между складами', 'code': 'warehouse_transfer', 'description': 'Перемещение товаров между складами'},
            {'name': 'Физ. лицо', 'code': 'personal', 'description': 'Доставка физическому лицу'},
            {'name': 'Юр. лицо', 'code': 'business', 'description': 'Доставка юридическому лицу'},
            {'name': 'Мед. товары', 'code': 'medical', 'description': 'Доставка медицинских товаров'},
            {'name': 'Хрупкий груз', 'code': 'fragile', 'description': 'Доставка хрупких товаров'},
            {'name': 'Температурный режим', 'code': 'temperature', 'description': 'Доставка с поддержанием температурного режима'},
        ]
        
        for service_data in services:
            Service.objects.get_or_create(
                code=service_data['code'],
                defaults={
                    'name': service_data['name'],
                    'description': service_data['description'],
                    'active': True,
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(services)} услуг'))
    
    def _create_delivery_statuses(self):
        """Создание справочника статусов доставки"""
        statuses = [
            {'name': 'В ожидании', 'code': 'pending', 'description': 'Доставка ожидает выполнения'},
            {'name': 'Проведено', 'code': 'completed', 'description': 'Доставка успешно завершена'},
        ]
        
        for status_data in statuses:
            DeliveryStatus.objects.get_or_create(
                code=status_data['code'],
                defaults={
                    'name': status_data['name'],
                    'description': status_data['description'],
                    'active': True,
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(statuses)} статусов доставки'))
    
    def _create_cargo_types(self):
        """Создание справочника типов груза"""
        cargo_types = [
            {'name': 'Стандартный', 'code': 'standard', 'description': 'Обычный груз'},
            {'name': 'Хрупкий', 'code': 'fragile', 'description': 'Хрупкий груз, требует осторожного обращения'},
            {'name': 'Тяжелый', 'code': 'heavy', 'description': 'Тяжелый груз (более 50 кг)'},
            {'name': 'Опасный', 'code': 'dangerous', 'description': 'Опасные вещества и материалы'},
            {'name': 'Скоропортящийся', 'code': 'perishable', 'description': 'Скоропортящиеся продукты и товары'},
        ]
        
        for type_data in cargo_types:
            CargoType.objects.get_or_create(
                code=type_data['code'],
                defaults={
                    'name': type_data['name'],
                    'description': type_data['description'],
                    'active': True,
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(cargo_types)} типов груза'))
    
    def _create_sample_deliveries(self):
        """Создание примеров доставок"""
        # Получаем справочники
        transport_models = list(TransportModel.objects.all())
        packaging_types = list(PackagingType.objects.all())
        services_list = list(Service.objects.all())
        pending_status = DeliveryStatus.objects.get(code='pending')
        completed_status = DeliveryStatus.objects.get(code='completed')
        cargo_types = list(CargoType.objects.all())
        
        # Создаем тестового пользователя, если надо
        admin_user = User.objects.get(username='admin')
        
        # Создаем доставки
        for i in range(1, 20):
            # Случайные данные
            transport_model = random.choice(transport_models)
            packaging = random.choice(packaging_types)
            status = random.choice([pending_status, pending_status, completed_status])  # 2/3 вероятность pending
            condition = random.choice(['Исправно', 'Исправно', 'Исправно', 'Неисправно'])  # 3/4 вероятность Исправно
            cargo_type = random.choice(cargo_types) if random.random() > 0.3 else None  # 70% вероятность иметь тип груза
            
            # Даты и время
            now = timezone.now()
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            departure_time = now - timedelta(days=days_ago, hours=hours_ago)
            
            # Время в пути: от 30 минут до 5 часов
            travel_hours = random.randint(1, 10) / 2  # 0.5, 1, 1.5, 2, 2.5, ... 5
            arrival_time = departure_time + timedelta(hours=travel_hours)
            
            # Дистанция: от 1 до 100 км
            distance = Decimal(round(random.uniform(1, 100), 2))
            
            # Создаем доставку
            delivery = Delivery.objects.create(
                number=f"{transport_model.code.upper()}-{100 + i}",
                transport_model=transport_model,
                departure_time=departure_time,
                arrival_time=arrival_time,
                distance=distance,
                packaging=packaging,
                status=status,
                condition=condition,
                cargo_type=cargo_type,
                created_by=admin_user,
                updated_by=admin_user,
            )
            
            # Добавляем случайные услуги (от 1 до 3)
            num_services = random.randint(1, 3)
            selected_services = random.sample(services_list, num_services)
            delivery.services.set(selected_services)
        
        self.stdout.write(self.style.SUCCESS('Создано 19 тестовых доставок')) 