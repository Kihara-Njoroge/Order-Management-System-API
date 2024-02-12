from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

base_urlpatterns = [
    path(
        "api/v1/",
        include(
            [
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path("docs/", SpectacularSwaggerView.as_view(url_name="schema")),
            ]
        ),
    ),
]

urlpatterns = base_urlpatterns + router.urls
