from rest_framework import serializers
from .models import Category, Product

class ProductCategoryReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for product categories
    """

    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class ProductReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for reading products
    """

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = '__all__'


class CreateProductSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating products
    """

    slug = serializers.SlugField(read_only=True)

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = "__all__"

    def validate_price(self, value):
        """
        Custom field-level validation for 'price'.
        """
        if value < 0:
            raise serializers.ValidationError("Price cannot be less than 0.")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Quantity cannot be less than 0.")
        return value

    def create(self, validated_data):
        category = validated_data.pop('category')
        product = Product.objects.create(**validated_data, category=category)
        return product

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            category = validated_data.pop('category')
            instance.category = category

        return super().update(instance, validated_data)
