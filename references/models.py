from django.db import models

# Create your models here.

class BaseReferenceModel(models.Model):
    """
    Базовая модель справочника
    
    Абстрактная модель для всех справочников с общими полями.
    """
    name = models.CharField('Название', max_length=100)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True, null=True)
    active = models.BooleanField('Активно', default=True)
    
    class Meta:
        abstract = True
        ordering = ['name']
    
    def __str__(self):
        return self.name


class TransportModel(BaseReferenceModel):
    """
    Справочник моделей транспорта
    
    Содержит информацию о видах и моделях транспортных средств,
    которые могут использоваться при доставке.
    """
    class Meta:
        verbose_name = 'Модель транспорта'
        verbose_name_plural = 'Модели транспорта'


class PackagingType(BaseReferenceModel):
    """
    Справочник типов упаковки
    
    Содержит информацию о различных типах упаковки,
    которые могут использоваться для груза.
    """
    class Meta:
        verbose_name = 'Тип упаковки'
        verbose_name_plural = 'Типы упаковки'


class Service(BaseReferenceModel):
    """
    Справочник услуг
    
    Содержит информацию о дополнительных услугах,
    которые могут быть предоставлены при доставке.
    """
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class DeliveryStatus(BaseReferenceModel):
    """
    Справочник статусов доставки
    
    Содержит возможные состояния процесса доставки
    (создана, в пути, доставлена, отменена и т.д.)
    """
    class Meta:
        verbose_name = 'Статус доставки'
        verbose_name_plural = 'Статусы доставки'


class CargoType(BaseReferenceModel):
    """
    Справочник типов груза
    
    Содержит классификацию грузов для правильного
    подбора транспорта и расчёта стоимости доставки.
    """
    class Meta:
        verbose_name = 'Тип груза'
        verbose_name_plural = 'Типы груза'
