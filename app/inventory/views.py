from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .filters import ProductFilter
from .models import Category, Product
from .serializers import (
    ProductCategoryReadSerializer,
    ProductReadSerializer,
    ProductWriteSerializer,
)

from .responses import Responses

response = Responses()

class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset for product categories.
    """

    queryset = Category.objects.all()
    serializer_class = ProductCategoryReadSerializer
    authentication_classes = []


class ProductReadViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for reading products.
    """

    queryset = Product.objects.all()
    serializer_class = ProductReadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class ProductWriteViewSet(viewsets.ModelViewSet):
    """
    Viewset for writing products.
    """

    queryset = Product.objects.all()
    serializer_class = ProductWriteSerializer

    def get_serializer_class(self):
        """
        Return the serializer class to use for the current request.
        """
        if self.action == "retrieve":
            return ProductReadSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            response.create_product_success(serializer.data),
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(response.get_products_success(serializer.data))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(response.get_products_success(serializer.data))

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(response.update_product_success(serializer.data))

    def destroy(self, request, pk=None):
        try:
            user = Product.objects.get(pk=pk)
            user.delete()
            return Response(response.delete_product_success(pk))
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
