from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Product


class ProductFilter(filters.FilterSet):
    product_name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )

    category_name = filters.CharFilter(
        field_name='category__name',
        lookup_expr='icontains',
    )

    class Meta:
        model = Product
        fields = ['product_name', 'category_name']
