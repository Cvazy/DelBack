from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TransportModelViewSet, PackagingTypeViewSet, ServiceViewSet,
    DeliveryStatusViewSet, CargoTypeViewSet, DeliveryViewSet,
    delivery_reports
)

router = DefaultRouter()
router.register(r'transport-models', TransportModelViewSet)
router.register(r'packaging-types', PackagingTypeViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'delivery-statuses', DeliveryStatusViewSet)
router.register(r'cargo-types', CargoTypeViewSet)
router.register(r'deliveries', DeliveryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reports/', delivery_reports, name='delivery-reports'),
]
