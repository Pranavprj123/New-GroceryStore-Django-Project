from django.urls import path
from order.views import checkout,payment_handler,order_details

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('payment-handler/', payment_handler, name='payment_handler'),
    path('order-details/<uuid:order_id>/', order_details, name='order_details'),
]