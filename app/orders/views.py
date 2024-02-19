from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem, OrderStatus
from .serializers import OrderItemSerializer, OrderReadSerializer, OrderWriteSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    Order items crud operations.
    """

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = []

    def get_queryset(self):
        """
        Get items in an order by order id.
        
        """
        res = super().get_queryset()
        order_id = self.kwargs.get('order_id')
        return res.filter(order__id=order_id)

    def perform_create(self, serializer):
        """
        Add items to an order
        
        """
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        serializer.save(order=order)


class OrderViewSet(viewsets.ModelViewSet):
    """
    Order crud operations.
    
    """
    queryset = Order.objects.all()
    permission_classes = []
    filter_backends = [filters.OrderingFilter]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return OrderWriteSerializer
        return OrderReadSerializer

    def get_queryset(self):
        """
        List orders.
        
        """
        res = super().get_queryset()
        status_param = self.request.query_params.get('status')
        if status_param:
            res = res.filter(status=status_param)
        return res


    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        """
        Place an order.
        
        """
        order = self.get_object()

        if order.status == OrderStatus.COMPLETED.value:
            return Response(
                {"error": "This order has already been completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if order.status == OrderStatus.PLACED.value:
            return Response(
                {"error": "This order has already been placed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order.status = OrderStatus.PENDING.value
        order.save()

        return Response(
            {"message": "Order placed successfully. You will receive a confirmation message shortly."},
            status=status.HTTP_200_OK,
        )
