from django.urls import path
from .views import delivery_reports

urlpatterns = [
    path('delivery-reports/', delivery_reports, name='delivery-reports'),
] 