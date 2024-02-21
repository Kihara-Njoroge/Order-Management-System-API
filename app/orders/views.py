from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderItemSerializer, ViewOrderSerializer, CreateOrderSerializer
from .tasks import send_order_confirmation_sms


class OrderItemViewSet(viewsets.ModelViewSet):
    """
     Order items CRUD oeprations
     
    """

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        res = super().get_queryset()
        order_id = self.kwargs.get('order_id')
        return res.filter(order__id=order_id)

    def perform_create(self, serializer):
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        serializer.save(order=order)


class OrderViewSet(viewsets.ModelViewSet):
    """
    Order CRUD Operations
    
    """

    queryset = Order.objects.all()
    authentication_classes = []
    permission_classes = []
    filter_backends = [filters.OrderingFilter]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return CreateOrderSerializer
        return ViewOrderSerializer

    def get_queryset(self):
        res = super().get_queryset()
        status_param = self.request.query_params.get('status')
        if status_param:
            res = res.filter(status=status_param)
        return res

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        order = self.get_object()
        if order.status == "COMPLETED":
            return Response(
                {"error": "This order has already been completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if order.status == "PLACED":
            return Response(
                {"error": "This order has already been placed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order.status = "PLACED"
        order.save()
        send_order_confirmation_sms(order.id)
        return Response(
            {"message": "Order placed successfully. You will receive a confirmation message shortly."},
            status=status.HTTP_200_OK,
        )
