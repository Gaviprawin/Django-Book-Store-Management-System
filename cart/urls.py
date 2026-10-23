
from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_detail, name="cart-detail"),
    path("add/<int:book_id>/", views.cart_add, name="cart-add"),
    path("update/<int:book_id>/", views.cart_update, name="cart-update"),
    path("remove/<int:book_id>/", views.cart_remove, name="cart-remove"),
]
