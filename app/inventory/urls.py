from django.urls import path, include
from rest_framework import routers
from .views import ProductCategoryViewSet, ProductWriteViewSet, ProductReadViewSet

router = routers.DefaultRouter()
router.register(r'categories', ProductCategoryViewSet)
router.register(r'products', ProductWriteViewSet)
router.register(r'products', ProductReadViewSet)

urlpatterns = [
    path('', include(router.urls)),
]