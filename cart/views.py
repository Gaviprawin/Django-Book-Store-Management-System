
from decimal import Decimal

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from books.models import Book


CART_SESSION_KEY = "cart"


def get_cart_data(request):
    cart = request.session.get(CART_SESSION_KEY, {})
    cart_items = []
    subtotal = Decimal("0.00")

    for book_id, quantity in cart.items():
        try:
            book = Book.objects.get(pk=int(book_id))
            quantity = int(quantity)

            if quantity < 1:
                continue

            line_total = book.price * quantity
            cart_items.append({
                "book": book,
                "quantity": quantity,
                "line_total": line_total,
            })
            subtotal += line_total
        except (Book.DoesNotExist, ValueError, TypeError):
            continue

    return cart_items, subtotal


def cart_detail(request):
    cart_items, subtotal = get_cart_data(request)

    return render(
        request,
        "cart/cart_detail.html",
        {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "total": subtotal,
        },
    )


@require_POST
def cart_add(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.")
        return redirect("book-detail", pk=book.pk)

    if book.stock < 1:
        messages.error(request, "This book is out of stock.")
        return redirect("book-detail", pk=book.pk)

    cart = request.session.get(CART_SESSION_KEY, {})
    current_quantity = int(cart.get(str(book.pk), 0))
    new_quantity = current_quantity + quantity

    if new_quantity > book.stock:
        messages.error(
            request,
            f"Only {book.stock} copies of {book.title} are available.",
        )
    else:
        cart[str(book.pk)] = new_quantity
        request.session[CART_SESSION_KEY] = cart
        request.session.modified = True
        messages.success(request, "Book added to cart!")

    return redirect("cart-detail")


@require_POST
def cart_update(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        messages.error(request, "Enter a valid quantity.")
        return redirect("cart-detail")

    cart = request.session.get(CART_SESSION_KEY, {})

    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.")
    elif quantity > book.stock:
        messages.error(
            request,
            f"Only {book.stock} copies of {book.title} are available.",
        )
    elif str(book.pk) in cart:
        cart[str(book.pk)] = quantity
        request.session[CART_SESSION_KEY] = cart
        request.session.modified = True
        messages.success(request, "Cart quantity updated.")

    return redirect("cart-detail")


@require_POST
def cart_remove(request, book_id):
    cart = request.session.get(CART_SESSION_KEY, {})
    cart.pop(str(book_id), None)

    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

    messages.success(request, "Item removed from cart.")
    return redirect("cart-detail")
