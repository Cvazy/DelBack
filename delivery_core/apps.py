from django.apps import AppConfig


class DeliveryCoreConfig(AppConfig):
    """
    Конфигурация приложения доставки
    
    Содержит настройки для приложения, управляющего основными
    бизнес-процессами доставки грузов.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'delivery_core'
    verbose_name = 'Доставки'
