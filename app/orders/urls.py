from django.urls import include, path
from rest_framework import routers

from .views import OrderItemViewSet, OrderViewSet


router = routers.DefaultRouter()
router.register(r'', OrderViewSet)
router.register(r'^(?P<order_id>\d+)/items', OrderItemViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
