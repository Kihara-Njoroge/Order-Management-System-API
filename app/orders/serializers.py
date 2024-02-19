import uuid

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer class for serializing order items
    """

    price = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'order',
            'product',
            'product_name',
            'quantity',
            'price',
            'amount',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('order',)

    def validate(self, validated_data):
        order_quantity = validated_data['quantity']
        product_quantity = validated_data['product'].quantity

        order_id = self.context['view'].kwargs.get('order_id')
        product = validated_data['product']
        current_item = OrderItem.objects.filter(order__id=order_id, product=product)

        if order_quantity > product_quantity:
            error = {'quantity': _('Ordered quantity is more than the available quantity.')}
            raise serializers.ValidationError(error)

        return validated_data

    def get_price(self, obj):
        return obj.product.price

    def get_amount(self, obj):
        return obj.amount

    def get_product_name(self, obj):
        return obj.product.name


class OrderReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for reading orders
    """

    customer = serializers.CharField(source='customer.get_full_name', read_only=True)
    order_items = OrderItemSerializer(read_only=True, many=True)
    total_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'customer',
            'tracking_number',
            'order_items',
            'total_amount',
            'status',
            'created_at',
            'updated_at',
        )

    def get_total_amount(self, obj):
        return obj.total_amount


class OrderWriteSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating orders and order items
    """

    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'status', 'order_items', 'created_at', 'updated_at', 'tracking_number')
        read_only_fields = ('status', 'tracking_number')

    def create(self, validated_data):
        orders_data = validated_data.pop('order_items')
        tracking_number = str(uuid.uuid4())
        validated_data['tracking_number'] = tracking_number
        order = Order.objects.create(**validated_data)

        for order_data in orders_data:
            OrderItem.objects.create(order=order, **order_data)

        return order

    def update(self, instance, validated_data):
        orders_data = validated_data.pop('order_items', None)
        orders = list((instance.order_items).all())

        if orders_data:
            for order_data in orders_data:
                order = orders.pop(0)
                order.product = order_data.get('product', order.product)
                order.quantity = order_data.get('quantity', order.quantity)
                order.save()

        return instance
