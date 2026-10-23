
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404

from .models import Category
from .forms import CategoryForm


def staff_required(view_func):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_staff
    )(view_func)


@staff_required
def category_list(request):
    categories = Category.objects.all()
    return render(
        request,
        "categories/category_list.html",
        {"categories": categories},
    )


@staff_required
def category_create(request):
    form = CategoryForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category created successfully!")
        return redirect("category-list")

    return render(
        request,
        "categories/category_form.html",
        {"form": form, "title": "Add Category"},
    )


@staff_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category updated successfully!")
        return redirect("category-list")

    return render(
        request,
        "categories/category_form.html",
        {"form": form, "title": "Edit Category"},
    )


@staff_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        try:
            category.delete()
            messages.success(request, "Category deleted successfully!")
        except ProtectedError:
            messages.error(
                request,
                "This category contains books. Move or delete those books first.",
            )

        return redirect("category-list")

    return render(
        request,
        "categories/category_confirm_delete.html",
        {"category": category},
    )
