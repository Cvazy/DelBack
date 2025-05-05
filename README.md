# Система управления доставками

## Описание проекта
Система предназначена для управления процессами доставки грузов. Включает функционал для создания, отслеживания 
и анализа доставок, а также управления справочной информацией.

## Архитектура проекта
Проект разделен на несколько модулей:

1. **references** - справочники системы
   - Модели транспорта
   - Типы упаковки
   - Услуги
   - Статусы доставки
   - Типы грузов

2. **delivery_core** - ядро системы доставки
   - Управление доставками
   - Основная бизнес-логика

3. **reports** - модуль отчетности
   - Генерация статистических отчетов по доставкам

## Установка и запуск

### Требования
- Python 3.8+
- Django 4.0+
- Django REST Framework 3.14+

### Подготовка к запуску
1. Клонируйте репозиторий
2. Создайте виртуальное окружение и активируйте его:
   ```
   python -m venv venv
   source venv/bin/activate  # для Linux/Mac
   venv\Scripts\activate     # для Windows
   ```
3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
4. Создайте файл .env в корне проекта и добавьте:
   ```
   DJANGO_SECRET_KEY=ваш_секретный_ключ
   ```

### Миграции базы данных
```
python manage.py migrate
```

### Создание базовых справочников
```
python manage.py setup_references
```

### Создание пользователя-администратора
```
python manage.py createsuperuser
```

### Запуск сервера
```
python manage.py runserver
```

## API Endpoints

### Аутентификация
- `POST /api/token/` - получение JWT токена
- `POST /api/token/refresh/` - обновление JWT токена
- `POST /api/token/verify/` - проверка JWT токена

### Справочники
- `GET /api/references/transport-models/` - список моделей транспорта
- `GET /api/references/packaging-types/` - список типов упаковки
- `GET /api/references/services/` - список услуг
- `GET /api/references/delivery-statuses/` - список статусов доставки
- `GET /api/references/cargo-types/` - список типов груза

Для каждого справочника также доступны операции CRUD по ID:
- `GET /api/references/{справочник}/{id}/` - получение записи
- `PUT /api/references/{справочник}/{id}/` - обновление записи
- `PATCH /api/references/{справочник}/{id}/` - частичное обновление записи
- `DELETE /api/references/{справочник}/{id}/` - удаление записи

### Доставки
- `GET /api/delivery/deliveries/` - список доставок
- `POST /api/delivery/deliveries/` - создание доставки
- `GET /api/delivery/deliveries/{id}/` - получение доставки
- `PUT /api/delivery/deliveries/{id}/` - обновление доставки
- `PATCH /api/delivery/deliveries/{id}/` - частичное обновление доставки
- `DELETE /api/delivery/deliveries/{id}/` - удаление доставки

Дополнительные действия:
- `POST /api/delivery/deliveries/{id}/mark_completed/` - отметить доставку как выполненную
- `GET /api/delivery/deliveries/stats/` - получить статистику по доставкам

### Отчеты
- `GET /api/reports/delivery-reports/` - получить отчеты по доставкам

## Параметры запросов

### Фильтрация доставок
- `?transport_model={id}` - фильтр по модели транспорта
- `?status={id}` - фильтр по статусу доставки
- `?packaging={id}` - фильтр по типу упаковки
- `?condition={value}` - фильтр по состоянию (Исправно/Неисправно)
- `?cargo_type={id}` - фильтр по типу груза
- `?min_distance={value}` - минимальная дистанция
- `?max_distance={value}` - максимальная дистанция
- `?services={id1,id2,...}` - фильтр по услугам
- `?time_filter=today|week` - фильтр по времени

### Параметры отчетов
- `?start_date={YYYY-MM-DD}` - начальная дата периода
- `?end_date={YYYY-MM-DD}` - конечная дата периода
- `?report_type=daily|weekly|monthly` - тип группировки по времени 