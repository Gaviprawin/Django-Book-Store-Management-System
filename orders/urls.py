from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout, name="order-checkout"),
    path("history/", views.order_history, name="order-history"),
    path("<int:pk>/", views.order_detail, name="order-detail"),
    path(
        "<int:pk>/status/",
        views.update_order_status,
        name="order-status-update",
    ),
]
