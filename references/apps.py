from django.apps import AppConfig


class ReferencesConfig(AppConfig):
    """
    Конфигурация приложения справочников
    
    Содержит настройки для приложения, управляющего справочниками
    системы доставки: модели транспорта, типы упаковки, услуги и др.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'references'
    verbose_name = 'Справочники'
