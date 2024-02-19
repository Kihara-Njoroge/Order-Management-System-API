from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from enum import Enum, unique
from inventory.models import Product
from accounts.models import CustomUser

@unique
class OrderStatus(Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    @classmethod
    def choices(cls):
        return [(status.value, _(status.name.lower())) for status in cls]


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(choices=OrderStatus.choices(), default=OrderStatus.PENDING.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.customer.get_full_name()

    @cached_property
    def total_amount(self):
        """
        Total amount of an order
        
        """
        return round(sum([order_item.cost for order_item in self.order_items.all()]), 2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="product_orders", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.order.customer.get_full_name()

    @cached_property
    def amount(self):
        """
        Total cost of the ordered item
        
        """
        return round(self.quantity * self.product.price, 2)
