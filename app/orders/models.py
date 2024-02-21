from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from inventory.models import Product
from enum import Enum

User = get_user_model()

class OrderStatus(Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    PLACED = 'PLACED'

class Order(models.Model):
    STATUS_CHOICES = [
        (OrderStatus.PENDING.value, _('pending')),
        (OrderStatus.COMPLETED.value, _('completed')),
        (OrderStatus.PLACED.value, _('placed')),
    ]

    customer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default=OrderStatus.PENDING.value, max_length=20)
    order_no = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.customer.get_full_name

    @cached_property
    def total_amount(self):
        """
        Total amount of all the items in an order
        """
        return round(sum([order_item.amount for order_item in self.order_items.all()]), 2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="product_orders", on_delete=models.CASCADE)
    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.order.customer.get_full_name

    @cached_property
    def amount(self):
        """
        Total amount of the ordered item
        """
        return round(self.quantity * self.product.price, 2)
