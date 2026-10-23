
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from books.models import Book
from cart.views import CART_SESSION_KEY
from .models import Order, OrderItem
from .forms import CheckoutForm


@login_required
def checkout(request):
    cart = request.session.get(CART_SESSION_KEY, {})

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect("cart-detail")

    form = CheckoutForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                locked_books = {}
                order_lines = []
                total = Decimal("0.00")

                # Lock and validate every book before creating the order.
                for book_id, quantity in cart.items():
                    try:
                        book_id = int(book_id)
                        quantity = int(quantity)
                    except (ValueError, TypeError):
                        raise ValueError("Invalid cart item. Please update your cart.")

                    if quantity < 1:
                        raise ValueError("Invalid quantity in cart.")

                    book = (
                        Book.objects.select_for_update()
                        .filter(pk=book_id)
                        .first()
                    )

                    if book is None:
                        raise ValueError(
                            "A book in your cart no longer exists. Please review your cart."
                        )

                    if quantity > book.stock:
                        raise ValueError(
                            f"Only {book.stock} copies of {book.title} are available. "
                            "Please update your cart."
                        )

                    locked_books[book_id] = book
                    line_total = book.price * quantity
                    order_lines.append((book, quantity, line_total))
                    total += line_total

                # Create the order only after every stock check succeeds.
                order = Order.objects.create(
                    user=request.user,
                    total_amount=total,
                    shipping_address=form.cleaned_data["shipping_address"],
                    phone=form.cleaned_data["phone"],
                )

                for book, quantity, line_total in order_lines:
                    OrderItem.objects.create(
                        order=order,
                        book=book,
                        book_title=book.title,
                        unit_price=book.price,
                        quantity=quantity,
                        subtotal=line_total,
                    )

                    book.stock -= quantity
                    book.save(update_fields=["stock"])

        except ValueError as error:
            messages.error(request, str(error))
            return redirect("cart-detail")

        request.session[CART_SESSION_KEY] = {}
        request.session.modified = True

        messages.success(request, "Order placed successfully!")
        return redirect("order-detail", pk=order.pk)

    return render(
        request,
        "orders/checkout.html",
        {"form": form},
    )


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/order_history.html", {"orders": orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    # Customers can only access their own orders.
    if order.user_id != request.user.id and not request.user.is_staff:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    return render(request, "orders/order_detail.html", {"order": order})


@user_passes_test(lambda user: user.is_authenticated and user.is_staff)
@require_POST
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get("status", "")

    allowed_statuses = {choice[0] for choice in Order.STATUS_CHOICES}

    if new_status not in allowed_statuses:
        messages.error(request, "Invalid order status.")
    elif order.status == Order.STATUS_CANCELLED:
        messages.error(request, "A cancelled order cannot be changed here.")
    else:
        order.status = new_status
        order.save(update_fields=["status", "updated_at"])
        messages.success(request, "Order status updated.")

    return redirect("order-detail", pk=order.pk)
