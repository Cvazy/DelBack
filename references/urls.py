from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TransportModelViewSet, PackagingTypeViewSet, ServiceViewSet,
    DeliveryStatusViewSet, CargoTypeViewSet,
)

router = DefaultRouter()
router.register(r'transport-models', TransportModelViewSet)
router.register(r'packaging-types', PackagingTypeViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'delivery-statuses', DeliveryStatusViewSet)
router.register(r'cargo-types', CargoTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 