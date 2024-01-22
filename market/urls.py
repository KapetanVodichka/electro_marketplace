from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import MarketConfig
from .views import NetworkElementViewSet, ProductViewSet, ContactsViewSet, SupplierViewSet

app_name = MarketConfig.name

router = DefaultRouter()
router.register(r'network-elements', NetworkElementViewSet, basename='networkelement')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'contacts', ContactsViewSet, basename='contacts')
router.register(r'suppliers', SupplierViewSet, basename='supplier')

urlpatterns = [
    path('', include(router.urls)),
]
