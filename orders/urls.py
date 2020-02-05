from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.index, name="index"),
    path("order/", views.order, name="order"),
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("my_orders/<int:id>", views.my_orders, name="my_orders")
]
