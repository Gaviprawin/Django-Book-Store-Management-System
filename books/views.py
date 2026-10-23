
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Book
from .forms import BookForm
from categories.models import Category


def book_list(request):
    books = Book.objects.select_related("category").all()
    categories = Category.objects.all()

    search = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "")
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    sort = request.GET.get("sort", "newest")

    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search)
        )

    if category_id.isdigit():
        books = books.filter(category_id=int(category_id))

    errors = []

    if min_price:
        try:
            value = Decimal(min_price)
            if value < 0:
                raise InvalidOperation
            books = books.filter(price__gte=value)
        except InvalidOperation:
            errors.append("Minimum price must be a valid non-negative number.")

    if max_price:
        try:
            value = Decimal(max_price)
            if value < 0:
                raise InvalidOperation
            books = books.filter(price__lte=value)
        except InvalidOperation:
            errors.append("Maximum price must be a valid non-negative number.")

    sort_options = {
        "newest": "-created_at",
        "oldest": "created_at",
        "price_low": "price",
        "price_high": "-price",
        "title": "title",
    }

    books = books.order_by(sort_options.get(sort, "-created_at"))

    return render(
        request,
        "books/book_list.html",
        {
            "books": books,
            "categories": categories,
            "search": search,
            "selected_category": category_id,
            "min_price": min_price,
            "max_price": max_price,
            "sort": sort,
            "filter_errors": errors,
        },
    )


def book_detail(request, pk):
    book = get_object_or_404(
        Book.objects.select_related("category"),
        pk=pk,
    )
    return render(request, "books/book_detail.html", {"book": book})


@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect("book-list")
    else:
        form = BookForm()

    return render(request, "books/book_form.html", {"form": form})


@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect("book-detail", pk=book.pk)
    else:
        form = BookForm(instance=book)

    return render(
        request,
        "books/book_form.html",
        {"form": form, "book": book},
    )


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted successfully!")
        return redirect("book-list")

    return render(
        request,
        "books/book_confirm_delete.html",
        {"book": book},
    )
