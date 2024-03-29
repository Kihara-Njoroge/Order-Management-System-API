from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from .views import SpectacularRapiDocView


router = DefaultRouter()

base_urlpatterns = [
    path(
        "api/v1/",
        include(
            [
                path("admin/", admin.site.urls),
                path('', include('users.urls')),
                path('', include('inventory.urls')),
                path('orders/', include('orders.urls')),
                path('schema/', SpectacularAPIView.as_view(), name='schema'),
                path("docs/", SpectacularRapiDocView.as_view(), name="api-docs"),
                path('prometheus/', include('django_prometheus.urls')),
            ]
        ),
    ),
]

urlpatterns = base_urlpatterns + router.urls
