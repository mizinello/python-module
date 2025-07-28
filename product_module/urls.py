from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, landing_page

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('landing/', landing_page, name='product-landing'),
]

