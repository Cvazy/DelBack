from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """
    Конфигурация приложения отчетов
    
    Предоставляет настройки для приложения, отвечающего за генерацию
    и предоставление различных отчетов по доставкам.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reports'
    verbose_name = 'Отчеты'
