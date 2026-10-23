from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "isbn",
        "price",
        "category",
        "stock",
    )

    search_fields = ("title", "author", "isbn")
    list_filter = ("category",)
    list_editable = ("price", "stock")