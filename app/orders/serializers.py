import uuid

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from .models import Order, OrderItem
from accounts.models import User


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
        product_quantity = validated_data['product'].stock

        order_id = self.context['view'].kwargs.get('order_id')
        product = validated_data['product']
        current_item = OrderItem.objects.filter(order__id=order_id, product=product)

        if order_quantity > product_quantity:
            error = {'quantity': _('Ordered quantity is more than the stock.')}
            raise serializers.ValidationError(error)

        if not self.instance and current_item.count() > 0:
            error = {'product': _('Product already exists in your order.')}
            raise serializers.ValidationError(error)

        return validated_data

    def get_price(self, obj):
        return obj.product.price

    def get_amount(self, obj):
        return obj.amount

    def get_product_name(self, obj):
        return obj.product.name


class ViewOrderSerializer(serializers.ModelSerializer):
    """
    Serializer class for reading orders
    """

    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    order_items = OrderItemSerializer(read_only=True, many=True)
    total_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'customer',
            'order_no',
            'order_items',
            'total_amount',
            'status',
            'created_at',
            'updated_at',
        )

    def get_total_amount(self, obj):
        return obj.total_amount


class CreateOrderSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating orders and order items
    
    """

    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'status', 'order_items', 'created_at', 'updated_at', 'order_no')
        read_only_fields = ('status', 'order_no')

    def create(self, validated_data):
        orders_data = validated_data.pop('order_items')
        order_no = str(uuid.uuid4())
        validated_data['order_no'] = order_no
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
