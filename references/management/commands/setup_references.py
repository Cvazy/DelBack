from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from decimal import Decimal

from references.models import (
    TransportModel, PackagingType, Service, 
    DeliveryStatus, CargoType
)
from delivery_core.models import Delivery


class Command(BaseCommand):
    """
    Команда для создания базовых записей в справочниках
    
    Эта команда создает необходимый минимум записей в справочниках,
    которые требуются для корректной работы системы.
    """
    help = 'Создает базовые записи в справочниках и тестовые доставки'

    def handle(self, *args, **kwargs):
        """
        Основной метод, выполняющий команду
        """
        self.stdout.write('Начинаем настройку базовых справочников...')
        
        # Статусы доставки
        statuses = [
            {'name': 'Создана', 'code': 'created', 'description': 'Доставка создана, но еще не начата'},
            {'name': 'В пути', 'code': 'in_progress', 'description': 'Доставка выполняется в данный момент'},
            {'name': 'Проведено', 'code': 'completed', 'description': 'Доставка успешно завершена'},
            {'name': 'Отменена', 'code': 'cancelled', 'description': 'Доставка отменена'},
            {'name': 'Задержана', 'code': 'delayed', 'description': 'Доставка задерживается'}
        ]
        
        for status_data in statuses:
            DeliveryStatus.objects.get_or_create(
                code=status_data['code'],
                defaults=status_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Создано статусов доставки: {len(statuses)}'))
        
        # Типы транспорта
        transport_models = [
            {'name': 'Легковой автомобиль', 'code': 'car', 'description': 'Для небольших посылок и документов'},
            {'name': 'Грузовой фургон', 'code': 'van', 'description': 'Для средних грузов'},
            {'name': 'Грузовик', 'code': 'truck', 'description': 'Для крупных грузов'},
            {'name': 'Мотоцикл', 'code': 'motorcycle', 'description': 'Для быстрой доставки мелких товаров'},
            {'name': 'Велосипед', 'code': 'bicycle', 'description': 'Для экологичной доставки в центре города'}
        ]
        
        for model_data in transport_models:
            TransportModel.objects.get_or_create(
                code=model_data['code'],
                defaults=model_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Создано моделей транспорта: {len(transport_models)}'))
        
        # Типы упаковки
        packaging_types = [
            {'name': 'Коробка', 'code': 'box', 'description': 'Стандартная картонная коробка'},
            {'name': 'Конверт', 'code': 'envelope', 'description': 'Бумажный или пластиковый конверт'},
            {'name': 'Пленка', 'code': 'film', 'description': 'Защитная пленка'},
            {'name': 'Палета', 'code': 'pallet', 'description': 'Деревянная или пластиковая палета'},
            {'name': 'Контейнер', 'code': 'container', 'description': 'Металлический контейнер для крупных грузов'}
        ]
        
        for packaging_data in packaging_types:
            PackagingType.objects.get_or_create(
                code=packaging_data['code'],
                defaults=packaging_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Создано типов упаковки: {len(packaging_types)}'))
        
        # Типы грузов
        cargo_types = [
            {'name': 'Документы', 'code': 'documents', 'description': 'Деловые бумаги, контракты, договоры'},
            {'name': 'Электроника', 'code': 'electronics', 'description': 'Компьютеры, смартфоны, бытовая техника'},
            {'name': 'Продукты', 'code': 'food', 'description': 'Скоропортящиеся продукты питания'},
            {'name': 'Мебель', 'code': 'furniture', 'description': 'Крупногабаритная мебель'},
            {'name': 'Одежда', 'code': 'clothes', 'description': 'Предметы гардероба, текстиль'}
        ]
        
        for cargo_data in cargo_types:
            CargoType.objects.get_or_create(
                code=cargo_data['code'],
                defaults=cargo_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Создано типов груза: {len(cargo_types)}'))
        
        # Услуги
        services = [
            {'name': 'Страховка', 'code': 'insurance', 'description': 'Страхование груза на время доставки'},
            {'name': 'Экспресс-доставка', 'code': 'express', 'description': 'Ускоренная доставка в течение суток'},
            {'name': 'Отслеживание', 'code': 'tracking', 'description': 'Подробное отслеживание перемещения груза'},
            {'name': 'Упаковка', 'code': 'packaging', 'description': 'Профессиональная упаковка груза'},
            {'name': 'Погрузка-разгрузка', 'code': 'loading', 'description': 'Услуги по погрузке и разгрузке'}
        ]
        
        for service_data in services:
            Service.objects.get_or_create(
                code=service_data['code'],
                defaults=service_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Создано услуг: {len(services)}'))
        
        # Создание тестовых доставок
        self.stdout.write('Создаем тестовые доставки...')
        self._create_test_deliveries()
        
        self.stdout.write(self.style.SUCCESS('Настройка базовых справочников и тестовых доставок завершена!'))
    
    def _create_test_deliveries(self):
        """
        Создает тестовые доставки с разнообразными данными
        """
        # Проверяем существующие доставки
        existing_count = Delivery.objects.count()
        if existing_count >= 15:
            self.stdout.write(self.style.WARNING(f'Уже создано {existing_count} доставок, пропускаем генерацию...'))
            return
        
        # Получаем все необходимые модели для ссылок
        transport_models = list(TransportModel.objects.all())
        packaging_types = list(PackagingType.objects.all())
        statuses = list(DeliveryStatus.objects.all())
        cargo_types = list(CargoType.objects.all())
        all_services = list(Service.objects.all())
        
        # Проверка наличия данных в справочниках
        if not transport_models or not packaging_types or not statuses:
            self.stdout.write(self.style.ERROR('Не найдены записи в справочниках. Создайте их сначала.'))
            return
        
        # Генерация случайных доставок
        deliveries_to_create = []
        num_deliveries = 15  # Создаем 15 доставок
        
        for i in range(1, num_deliveries + 1):
            # Создаем случайное время отправления в диапазоне от 30 дней назад до текущего момента
            departure_time = timezone.now() - timedelta(days=random.randint(0, 30),
                                                       hours=random.randint(0, 23),
                                                       minutes=random.randint(0, 59))
            
            # Время в пути от 1 часа до 5 дней
            travel_duration = timedelta(hours=random.randint(1, 120))
            arrival_time = departure_time + travel_duration
            
            # Генерируем случайную дистанцию от 1 до 1500 км
            distance = Decimal(str(round(random.uniform(1, 1500), 2)))
            
            # Создаем доставку
            delivery = Delivery(
                number=f"D-{2024}-{i:05d}",  # уникальный номер
                transport_model=random.choice(transport_models),
                departure_time=departure_time,
                arrival_time=arrival_time,
                distance=distance,
                packaging=random.choice(packaging_types),
                status=random.choice(statuses),
                condition=random.choice(['Исправно', 'Неисправно']),
                cargo_type=random.choice(cargo_types) if random.random() > 0.2 else None,
                notes=f"Тестовая доставка #{i}" if random.random() > 0.5 else None
            )
            
            # Сохраняем доставку
            delivery.save()
            
            # Добавляем случайные услуги (от 0 до 3)
            num_services = random.randint(0, min(3, len(all_services)))
            selected_services = random.sample(all_services, num_services)
            for service in selected_services:
                delivery.services.add(service)
            
            deliveries_to_create.append(delivery)
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(deliveries_to_create)} тестовых доставок')) 