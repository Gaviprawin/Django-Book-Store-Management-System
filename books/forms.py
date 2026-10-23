
from django import forms
from .models import Book


class BookForm(forms.ModelForm):

    class Meta:
        model = Book

        fields = [
            "title",
            "author",
            "isbn",
            "price",
            "description",
            "category",
            "stock",
            "cover_image",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4}
            ),
            "price": forms.NumberInput(
                attrs={"min": "0.01", "step": "0.01"}
            ),
            "stock": forms.NumberInput(
                attrs={"min": "0", "step": "1"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"

    def clean_isbn(self):
        isbn = self.cleaned_data["isbn"].strip()

        if not isbn.isdigit() or len(isbn) not in (10, 13):
            raise forms.ValidationError(
                "ISBN must contain 10 or 13 digits."
            )

        return isbn

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price <= 0:
            raise forms.ValidationError(
                "Price must be greater than zero."
            )

        return price

    def clean_title(self):
        title = self.cleaned_data["title"].strip()

        if not title:
            raise forms.ValidationError(
                "Book title is required."
            )

        return title
