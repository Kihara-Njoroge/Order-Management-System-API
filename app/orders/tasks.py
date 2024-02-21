# tasks.py
from django.conf import settings
from .models import Order
import africastalking

def send_order_confirmation_sms(order_id):
    order = Order.objects.get(id=order_id)
    customer_phone = str(order.customer.phone_number)

    africastalking.initialize(
        settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY
    ),
    sms = africastalking.SMS

    message = f"Thank you for shopping with us! Your order tracking no. is {order.order_no}. Total Amount: {order.total_amount}."

    def on_finish(error, response):
        if error is not None:
            raise error
        print(response)
    sms.send(message, [customer_phone], callback=on_finish)
