# tasks.py
from django.conf import settings
from .models import Order
import africastalking

def send_order_confirmation_sms(order_id):
    order = Order.objects.get(id=order_id)
    buyer_phone = str(order.buyer.profile.phone_number)

    africastalking.initialize(
        settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY
    ),
    sms = africastalking.SMS

    message = f"Thank you for your order with us! Your order reference code is {order.ref}. Total cost: {order.total_cost}"

    def on_finish(error, response):
        if error is not None:
            raise error

    sms.send(message, [buyer_phone], callback=on_finish)
