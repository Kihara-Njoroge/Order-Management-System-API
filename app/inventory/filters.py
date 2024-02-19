from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Product, CategoryChoices


class ProductFilter(filters.FilterSet):
    product_name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )

    category_name = filters.CharFilter(
        field_name='category__name',
        lookup_expr='icontains',  
        method='filter_category_name',
    )

    def filter_category_name(self, queryset, name, value):
        return queryset.filter(category__name__icontains=value)

    class Meta:
        model = Product
        fields = ['product_name', 'category_name']
